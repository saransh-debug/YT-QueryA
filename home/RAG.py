from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi , TranscriptsDisabled
from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpointEmbeddings , HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda , RunnableParallel , RunnablePassthrough
from urllib.parse import parse_qs , urlparse
load_dotenv()


def video_id_extractor(link):
    parsed_url = urlparse(link)

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v",[None])[0]

    if parsed_url.hostname in ['youtu.be']:
        return parsed_url.path.lstrip("/")

    return None

    

def Rag(link , query):
    
    video_id = video_id_extractor(link)  # video link pasting

    if video_id is None:
        return f"No Video Id available for {link} " 
    yt_api = YouTubeTranscriptApi()

    res = yt_api.fetch(
        video_id= video_id, 
        languages=['en']
    )

    transcript = " ".join(i['text'] for i in res.to_raw_data())
    # print(transcript)

    Splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000 , 
        chunk_overlap = 200
    )

    docs = Splitter.create_documents([transcript])


    #-------------------------------------indexing----------------------------------------------------------------------
    embeddings = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.from_documents(
        documents=docs ,  
        embedding=embeddings

    )

    retriver = vector_store.as_retriever(search_type ="mmr" , search_kwargs={"k":4 ,"lambda_mult":0.2})

    # print(retriver.invoke("what are robots"))




    def context_extractor(result):
        # print(result)
        context = "\n\n".join(doc.page_content for doc in result)
        return context



    #-------------------------------------chaining-----------------------------------------------------------------
    parallel_chain = RunnableParallel(
        question = RunnablePassthrough() , 
        context = retriver| RunnableLambda(context_extractor)
    )

    # print(parallel_chain.invoke("what are robots?"))


    template = PromptTemplate(
        template="""
    You are a YouTube video Rag Tutor . Respond to the students or person's query in a professional manner .
    Avoid writing anything about yourself , start directly by answering the question of the user.

    Context:
    {context}

    Question:
    {question}
    """,
        input_variables=["context", "question"],
    )


    chatmodel = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        
    ) 

    llm = ChatHuggingFace(llm=chatmodel)

    parser = StrOutputParser()

    main_chain = parallel_chain | template | llm | parser



    return (main_chain.invoke(query))
    # print(main_chain.get_graph().print_ascii())



