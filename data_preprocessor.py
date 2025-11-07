import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter





def create_documents(profiles_data: list) -> list:
    documents = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    for profile in profiles_data:
        bio = profile.get("bio","")
        if isinstance(bio, list):
            bio = " ".join(bio)
        bio = bio.strip()    
        if not bio or (bio == "N/A"):
            bio = profile.get("expertise","N/A")
            if isinstance(bio,list):
                bio = " ".join(bio)
            bio = bio.strip()    

            if bio =="N/A":
                bio = profile.get("title","N/A").strip()
        metadata ={
            "name": profile.get("name","Unknown"),
            "title": profile.get("title","N/A"),
            "department": ", ".join(profile.get("department",[])),
            "email": profile.get("email","N/A"),
            "expertise": ", ".join(profile.get("expertise", [])),
            "profile_url": profile.get("profile_url", "N/A")}
        chunks = splitter.split_text(bio)
        for chunk in chunks:
            documents.append(Document(page_content=chunk,metadata=metadata))

        print(f"Created {len(chunks)} document chunks for profile: {profile['name']}")
    return documents

if __name__ == "__main__":
    input_file = "data_new/json/uw_profiles_data.json"
    output_file = "data_new/json/langchain_documents.json"

    # Load the profiles data
    with open(input_file, "r") as f:
        profiles_data = json.load(f)

    # Create LangChain Document objects
    documents = create_documents(profiles_data)

    # Save the documents to a JSON file
    with open(output_file, "w") as f:
        json.dump([doc.dict() for doc in documents], f, indent=4)

    print(f"LangChain documents saved to {output_file}")