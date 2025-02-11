FROM openjdk:17-alpine

COPY ./app/*.jar video2document.jar

ENTRYPOINT ["sh", "-c", "java -jar -DOPENAI_API_KEY=${OPENAI_API_KEY} video2document.jar"]
