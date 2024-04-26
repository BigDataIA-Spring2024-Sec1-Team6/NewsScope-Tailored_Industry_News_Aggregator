# NewsScope


## **Industry Specific News Aggregation Platform** - **NewsScope** : Tailored Industry News Aggregator


### **Project Overview** 

* NewsScope will provide a tailored news aggregation service that allows users to view and track headlines specifically filtered by industry, such as entertainment, sports, politics, technology and fashion

* The platform will aggregate news from multiple sources, presenting a comprehensive and up-to-date feed of industry-specific news, leveraging advanced technologies and tools

* This system works based on providing user-centric news headlines, based on the keywords searched by the user

* This platform will leverage cutting-edge NLQI and AI technologies to provide a highly personalized and context-aware experience

### **Technologies and Tools:**

![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)
![DBT](https://img.shields.io/badge/DBT-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Google Cloud Platform](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-13AA52?style=for-the-badge&logo=pinecone&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)


* **Data Collection:** Use BeautifulSoup for web scraping to collect news headlines from various online sources

* **Storage:** Snowflake for robust and scalable data management

* **Data Transformation:** Employ DBT for transforming and structuring scraped data, preparing it for access

* **Artificial Intelligence:** Leverage OpenAI to enhance content, such as generating summaries of articles and processing natural language queries

* **Vector Search:** Implement Pinecone to perform sophisticated search operations, allowing users to find related articles quickly based on their interests

* **User Interface:** Streamlit for a user-friendly front-end

* **Automation:** Apache Airflow for scheduling and orchestrating the ETL pipeline


### **Architecture Diagram**


![Final_ProjDiag2 drawio](https://github.com/BigDataIA-Spring2024-Sec1-Team6/FinalProj_Team6/assets/114605149/12287ef4-5dd3-4eb6-b5c9-9050b359a6bc)




### **Feature Design**

* **Multi-Source Compilation:**

  * To provide a well-rounded view of each industry by compiling news from various sources, ranging from mainstream media to niche industry journals
  * By aggregating multiple sources, the service minimizes bias and offers a more comprehensive understanding of each topic. Users benefit from gaining insights from different angles, which can aid in better decision-making and broader knowledge

* **Industry-Specific Filters:**

  * This feature allows users to tailor their news feeds to specific industries of interest, such as technology, finance, healthcare, or any other sector relevant to their professional or personal needs
  * Users receive highly relevant information, saving time and increasing efficiency by filtering out unrelated content. This targeted approach helps users stay informed about specific sectors, which is especially beneficial for professionals who need to keep up with industry trends and developments


* **Recommendation - Customized Keyword:**

  * Deliver personalized news experiences by providing news headlines that are directly relevant to the user's searched keywords
  * Increases user engagement by ensuring the news content is highly relevant to the user's interests. Enhances user satisfaction by tailoring content delivery to individual preferences, thus making news consumption more targeted and less time-consuming

* **Natural Language Query Search:**

  * Enhance user interaction with the platform by enabling them to perform complex queries using natural language, facilitating an intuitive and conversational interaction with the news aggregation service
  * The NLQI provides a deep contextual understanding of user queries, enabling the platform to tailor content curation beyond simple keyword matching

* **Article Summary:**

  * Aid users in quickly grasping the essence of lengthy documents, articles, or reports without the need to go through the entire text, which is especially useful in environments where time and quick understanding are of the essence
  * Leverage OpenAI's latest generative models, to provide concise, accurate summaries of extensive textual content



### **Deliverables**

* A fully functional news aggregation system that filters and displays news according to specific industries such as technology, healthcare, finance, sports, and more

* A sophisticated query-handling module capable of interpreting complex natural language inputs and returning highly relevant news articles

* A personalized recommendation engine that dynamically suggests news articles based on the user's keyword preferences

* Reduces information overload by distilling complex information into digestible summaries, enabling users to make faster and more informed decisions. Increases productivity by allowing users to consume more information in less time

### **TechStack**
Python| Streamlit| GitHub| Apache Airflow| Pinecone| Langchain| OpenAI| Docker| GCP|


### **Project Flow**

 Start by registering in our application to personalize your news experience. Once registered, log in to discover the specific features:
 
* Customized Keywords Recommendation :- If the user has a specific keywords in mind and wants news only related to those, he/she can store those keywords and the feed will only have similar content to it when he/she clicks on Recommend Headlines. If not, he /she can just click on Recommend Headlines to get the top news
* Industry Specific Filters :- If the user has a specific industry which he wants to watch, he/she can chose it and the page would be further displayed with only the news from the speicifc industries
* Summary Generation :- This is the page where he/she can select a specific industry and select a specific headline to summarize
* Natural Language Query Search :- User can enter a news search query to get a specific output

### **Learning Outcomes**

* Python Programming Proficiency: Gain deeper expertise in Python, particularly in utilizing libraries and managing virtual environments
Learn to write and maintain Python scripts effectively for various tasks including data collection, processing, and interacting with APIs

* Web Scraping and Data Collection: Learn how to use BeautifulSoup to scrape data from websites. Understand the legal and ethical considerations of web scraping

* Data Storage and Management: Gain hands-on experience with cloud storage solutions like AWS S3 for storing large datasets. Learn how to use Snowflake for data warehousing, executing SQL queries, and managing scalable database solutions

* Data Transformation: Develop skills in using DBT (data build tool) for transforming and structuring data in a Snowflake environment. Understand the principles of data modeling and ETL (Extract, Transform, Load) processes

* Artificial Intelligence: Learn to implement AI features using OpenAI, such as generating text summaries and retreiving relevant content corresponding to the search prompt

* Vector Search Implementation: Understand and implement vector search technology using Pinecone to handle sophisticated search operations, enabling quick retrieval of related articles based on vector similarities

* Building User Interfaces: Develop interactive web applications using Streamlit, enhancing user experience and making data-driven applications accessible

* Automation and Orchestration: Learn to automate and orchestrate workflows using Apache Airflow, managing the scheduling and execution of complex data pipelines efficiently

* Collaborative and Version Control Skills: Enhance proficiency in using Git for version control, enabling efficient collaboration in software development projects

### **Steps to run NewsScope :-**
* Clone the Github Repository on the VM on your Instance
* Install Docker on the VM on that instance
* Make sure your .env variables are set
* Make Sure in your streamlit folder , you have secrets.toml with your credentials
* Type "sudo make build-up" in your directory

You will be able to access the application on your specific IP from GCP


WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENT'S WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

| Name               | Contribution %   | Contributions                                                                          |
|--------------------|------------------|----------------------------------------------------------------------------------------|
| Osborne .V. Lopes  |     33.33%       | Data Collection with Beautiful Soup [web scrapping], Dockerisation & Hosting           |
| Akshita Pathania   |     33.33%       | UI development with Streamlit, OpenAI integration for NLQI, OpenAI summary generation  |
| Smithi Parthiban   |     33.33%       | Snowflake DB and table creation, DBT data transformation, OpenAI NLQI integration, OpenAI summary generation |
| Manimanya Reddy    |     33.33%       | Test case creation, Airflow automation, Hosting, Documentation                         |
 



**Final Project Proposal CodeLabs:** https://codelabs-preview.appspot.com/?file_id=1haYDcuQK1Oxnp8UQYAao4hnCNlk6h_lgOTI4obYumrI#0

**Final Project Codelab:** [https://codelabs-preview.appspot.com/?file_id=169lP8amGI_e_gYvi_ledgFYgdevNKTQijMiTe_b8FUQ#2](https://codelabs-preview.appspot.com/?file_id=169lP8amGI_e_gYvi_ledgFYgdevNKTQijMiTe_b8FUQ#4)

**Streamlit Deployment:** [34.74.168.206:8501](http://34.139.93.177:8501/)

**Airflow Deployment:** http://34.74.168.206:8080/home

**Youtube Demo Link:** https://youtu.be/PvtTSozvR1k



