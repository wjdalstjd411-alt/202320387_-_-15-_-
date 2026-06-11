# Hybrid Vector RAG & Graph RAG using Neo4j

## 1. 프로젝트 소개

본 프로젝트는 Retrieval-Augmented Generation(RAG)의 검색 성능을 개선하고 관계 기반 질의를 처리하기 위해 Vector RAG와 Graph RAG를 함께 구현한 시스템이다.

기존 Vector RAG는 의미적으로 유사한 문서를 검색하는 데 강점을 가지지만, 엔티티 간 관계를 추적하거나 다단계 추론(Multi-hop Reasoning)을 수행하는 데에는 한계가 존재한다.

이를 보완하기 위해 Neo4j 기반 Knowledge Graph를 구축하고 GraphCypherQAChain을 활용하여 자연어 질문을 Cypher Query로 변환하는 Graph RAG를 구현하였다.

또한 Dense Retrieval, Sparse Retrieval(BM25), Hybrid Retrieval을 구현하고 RAGAS를 활용하여 검색 품질과 답변 품질을 평가하였다.

---

## 2. 도메인 선택 이유

본 프로젝트는 기업, 인물, 대학교 간 관계 데이터를 활용하였다.

예시 질문은 다음과 같다.

* 삼성전자의 CEO는 누구인가?
* 삼성전자의 CEO가 졸업한 대학은 어디인가?
* 카카오의 자회사는 몇 개인가?
* 특정 기업의 투자 관계는 몇 개인가?

이러한 질문들은 단순 키워드 검색보다 관계 추적과 다단계 추론이 중요하다.

따라서 본 도메인은 langchain_neo4j.chains.graph_qa.cypher를 사용한 Graph RAG의 장점을 확인하기에 적합하다고 판단하였다.

---

## 3. 시스템 구조

### Vector RAG

Document Loader
→ Text Splitter
→ Embedding
→ Vector Store
→ Dense / Sparse / Hybrid Retrieval
→ LLM Answer Generation

### Graph RAG

CSV Data
→ Neo4j Graph
→ GraphCypherQAChain
→ Cypher Query
→ Graph Answer Generation

---

## 4. Document Loader 선택 근거

### CSVLoader

정형 데이터(기업, 인물, 대학, 관계 정보)를 로드하기 위해 사용하였다.

적재 데이터

* companies.csv
* people.csv
* universities.csv
* relations.csv

### JSONLoader

추가 기업 문서 데이터를 적재하기 위해 사용하였다.

이를 통해 과제 요구사항인 2종류 이상의 Loader를 충족하였다.

### Metadata 설계

모든 문서에는 다음 메타데이터를 포함하였다.

| Metadata | 설명       |
| -------- | -------- |
| source   | 원본 파일 경로 |
| type     | 문서 유형    |

예시

```python
{
  "source": "data/companies.csv",
  "type": "company"
}
```

---

## 5. Splitter 선택 근거

### RecursiveCharacterTextSplitter

* 안정적인 청크 생성
* 문단 → 문장 → 단어 순으로 분할
* 검색 정확도 향상

설정값

```python
chunk_size = 500
chunk_overlap = 50
```

선택 이유

* 청크가 너무 작으면 문맥 손실 발생
* 청크가 너무 크면 검색 정확도 감소
* 500/50은 문맥 유지와 검색 효율의 균형을 고려하여 선택

생성 청크 수

* Recursive: 185

---

### SemanticChunker

* 의미 기반 분할
* 유사한 문장을 하나의 청크로 묶음
* 문맥 보존 능력 향상

생성 청크 수

* Semantic: 166

---

## 6. Retriever 선택 근거

### Sparse Retrieval (BM25)

장점

* 키워드 검색에 강함
* 기업명, 인물명 검색에 유리

### Dense Retrieval

장점

* 의미 기반 검색 가능
* 동의어 및 유사 표현 검색 가능

### Hybrid Retrieval

장점

* Dense + Sparse 결합
* 검색 품질 향상

실험 결과 모든 RAGAS 지표에서 Dense Retrieval보다 우수한 성능을 보였다.

---

## 7. Graph Schema

### Node Types

| Node       | 설명  |
| ---------- | --- |
| Company    | 기업  |
| Person     | 인물  |
| University | 대학교 |

### Relationship Types

| Edge           | 설명     |
| -------------- | ------ |
| CEO_OF         | CEO 관계 |
| GRADUATED_FROM | 졸업 관계  |
| WORKS_AT       | 근무 관계  |
| FOUNDED        | 창업 관계  |

---

## 8. 실행 방법

### 1) 저장소 클론

```bash
git clone <repository_url>
cd project
```

---

### 2) 가상환경 생성

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

### 3) 패키지 설치

```bash
pip install -r requirements.txt
```

---

### 4) 환경변수 설정

프로젝트 루트에 .env 생성

```env
OPENAI_API_KEY=YOUR_KEY

NEO4J_URI=YOUR_URI
NEO4J_USERNAME=YOUR_USERNAME
NEO4J_PASSWORD=YOUR_PASSWORD
```

---

### 5) 데이터 적재

```bash
python ingestion/loaders.py
```

---

### 6) Graph 구축

```bash
python graph/build_graph.py
```

본 코드는 MERGE를 사용하므로 반복 실행해도 노드가 중복 생성되지 않는다.

---

### 7) Retrieval 테스트

Sparse

```bash
python retrieval/test_sparse.py
```

Dense

```bash
python retrieval/test_dense.py
```

Hybrid

```bash
python retrieval/test_hybrid.py
```

---

### 8) Graph QA

```bash
python graph/graph_qa.py
```

---

### 9) RAGAS 평가

Dense 답변 생성

```bash
python evaluation/generate_dense_answers.py
```

Hybrid 답변 생성

```bash
python evaluation/generate_hybrid_answers.py
```

평가 실행

```bash
python evaluation/ragas_eval.py
```

---

## 9. Neo4j 설정 가이드

### AuraDB

Neo4j AuraDB 무료 티어 생성

환경변수에 다음 정보 입력

```env
NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=
```

### Docker (대안)

```bash
docker run \
-p7474:7474 \
-p7687:7687 \
--name neo4j \
-e NEO4J_AUTH=neo4j/password \
neo4j:latest
```

Browser 접속

```text
http://localhost:7474
```

---

## 10. 평가 데이터셋

평가 데이터는 다음 파일에 포함되어 있다.

```text
testset.json
```

또는

```text
testset.csv
```

총 30개의 질문-정답 쌍으로 구성되어 있으며

* 사실 조회
* 관계 추적
* 집계 질의
* 다단계 추론

을 포함한다.

---

## 11. 확장 기능

구현한 확장 기능

1. Custom Evaluation Metric

   * 평균 응답시간 측정

2. Graph Visualization

   * Neo4j Browser 활용

3. LLMGraphTransformer 실험

   * 비정형 텍스트 자동 Graph 변환

---

## 12. 주요 결과

### Dense Retrieval

Faithfulness: 0.7000

Answer Relevancy: 0.4988

Context Precision: 0.4667

Context Recall: 0.4667

### Hybrid Retrieval

Faithfulness: 0.7667

Answer Relevancy: 0.5275

Context Precision: 0.4900

Context Recall: 0.5000

Hybrid Retrieval이 모든 평가 지표에서 Dense Retrieval보다 높은 성능을 보였다.
