from langchain_community.document_loaders import CSVLoader
import os


def load_csv_docs():

    files = [
        "data/companies.csv",
        "data/people.csv",
        "data/universities.csv",
        "data/relations.csv",
        "data/company_document.csv"
    ]

    docs = []

    for file in files:

        print(f"\n[LOADING] {file}")

        if not os.path.exists(file):
            print(f"[ERROR] 파일 없음 -> {file}")
            continue

        try:
            loader = CSVLoader(
                file_path=file,
                encoding="utf-8"
            )

            loaded_docs = loader.load()

            print(f"[SUCCESS] {len(loaded_docs)}개 문서 로드")

            for doc in loaded_docs:

                doc.metadata["source"] = file

                if "companies" in file:
                    doc.metadata["type"] = "company"

                elif "people" in file:
                    doc.metadata["type"] = "person"

                elif "universities" in file:
                    doc.metadata["type"] = "university"

                elif "relations" in file:
                    doc.metadata["type"] = "relation"

                elif "company_document" in file:
                    doc.metadata["type"] = "company_document"

            docs.extend(loaded_docs)

        except Exception as e:
            print(f"[ERROR] {file}")
            print(e)

    print(f"\n총 문서 수: {len(docs)}")

    return docs