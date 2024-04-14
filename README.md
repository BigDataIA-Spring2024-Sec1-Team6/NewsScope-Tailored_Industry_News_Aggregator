# FinalProj_Team6


**Industry Specific News Aggregation Platform** - **NewsScope** : Tailored Industry News Aggregator


**Project Overview**

* NewsScope will provide a tailored news aggregation service that allows users to view and track headlines specifically filtered by industry, such as entertainment, sports, space, and religion.

* The platform will aggregate news from multiple sources, presenting a comprehensive and up-to-date feed of industry-specific news, leveraging advanced technologies and tools.

* This system works based on providing user-centric news headlines, based on the keywords searched by the user.

* This platform will leverage cutting-edge NLQI and AI technologies to provide a highly personalized and context-aware experience.


**Architecture Diagram**

![Final_ProjDiag1 drawio](https://github.com/BigDataIA-Spring2024-Sec1-Team6/FinalProj_Team6/assets/114605149/f34ace7b-0c57-46f0-99ee-e9a61ed2cffd)




**Technologies and Tools:**

* **Data Collection:** Use BeautifulSoup for web scraping to collect news headlines from various online sources

* **Storage:** Snowflake and AWS S3 for robust and scalable data management

* **Data Transformation:** Employ DBT for transforming and structuring scraped data, preparing it for access

* **Artificial Intelligence:** Leverage OpenAI to enhance content, such as generating summaries of articles and processing natural language queries

* **Vector Search:** Implement Pinecone to perform sophisticated search operations, allowing users to find related articles quickly based on their interests

* **User Interface:** Streamlit for a user-friendly front-end

* **Automation:** Apache Airflow for scheduling and orchestrating the ETL pipeline



**Feature Design**

* **Multi-Source Compilation:**

  * To provide a well-rounded view of each industry by compiling news from various sources, ranging from mainstream media to niche industry journals.
  * By aggregating multiple sources, the service minimizes bias and offers a more comprehensive understanding of each topic. Users benefit from gaining insights from different angles, which can aid in better decision-making and broader knowledge.

* **Industry-Specific Filters:**

  * This feature allows users to tailor their news feeds to specific industries of interest, such as technology, finance, healthcare, or any other sector relevant to their professional or personal needs.
  * Users receive highly relevant information, saving time and increasing efficiency by filtering out unrelated content. This targeted approach helps users stay informed about specific sectors, which is especially beneficial for professionals who need to keep up with industry trends and developments.


* **Recommendation - Customized Keyword:**

  * Deliver personalized news experiences by providing news headlines that are directly relevant to the user's searched keywords.
  * Increases user engagement by ensuring the news content is highly relevant to the user's interests. Enhances user satisfaction by tailoring content delivery to individual preferences, thus making news consumption more targeted and less time-consuming.

* **Natural Language Query Search:**

  * Enhance user interaction with the platform by enabling them to perform complex queries using natural language, facilitating an intuitive and conversational interaction with the news aggregation service.
  * The NLQI provides a deep contextual understanding of user queries, enabling the platform to tailor content curation beyond simple keyword matching.

* **Article Summary:**

  * Aid users in quickly grasping the essence of lengthy documents, articles, or reports without the need to go through the entire text, which is especially useful in environments where time and quick understanding are of the essence.
  * Leverage OpenAI's latest generative models, to provide concise, accurate summaries of extensive textual content.



**Deliverables**

* A fully functional news aggregation system that filters and displays news according to specific industries such as technology, healthcare, finance, sports, and more.

* A sophisticated query-handling module capable of interpreting complex natural language inputs and returning highly relevant news articles.

* A personalized recommendation engine that dynamically suggests news articles based on the user's keyword preferences.

* Reduces information overload by distilling complex information into digestible summaries, enabling users to make faster and more informed decisions. Increases productivity by allowing users to consume more information in less time

**Resources and Team**
Akshita: User Interface development with Streamlit, OpenAI integration for NLQI

Osborne: Data Collection with Beautiful Soup, APIs, and data storage

Smithi: DBT data transformation, OpenAI NLQI integration, cloud hosting

Manya: Data validation, Airflow automation, Pinecone integration



**Final Project Project Proposal Codelabs:** https://codelabs-preview.appspot.com/?file_id=1haYDcuQK1Oxnp8UQYAao4hnCNlk6h_lgOTI4obYumrI#0


