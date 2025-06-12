package com.superlawva;

import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class BackApplication {
    public static void main(String[] args) {
        // back 폴더에 있는 .env를 직접 지정
        Dotenv dotenv = Dotenv.configure()
                .directory("back")
                .ignoreIfMalformed()
                .load();

        System.setProperty("SPRING_DATASOURCE_URL",      dotenv.get("SPRING_DATASOURCE_URL"));
        System.setProperty("SPRING_DATASOURCE_USERNAME", dotenv.get("SPRING_DATASOURCE_USERNAME"));
        System.setProperty("SPRING_DATASOURCE_PASSWORD", dotenv.get("SPRING_DATASOURCE_PASSWORD"));

        SpringApplication.run(BackApplication.class, args);
    }
}

