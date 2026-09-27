package com.hackathon.target.tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CheckoutApiTest {

    @LocalServerPort
    private int port;

    @BeforeAll
    public static void setup() {
        RestAssured.basePath = "/api/checkout";
    }

    @Test
    public void testCheckoutPriceCalculation() {
        RestAssured.port = port;
        // Change the JSON payload inside testCheckoutPriceCalculation() to a $200 item
        String requestBody = "{ \"price\": 200.0, \"discount\": 10.0 }";
        // The buggy controller will do 200 - 10 = 190. 
        // A real 10% discount should be 180. The test will now correctly FAIL.

        given()
                .contentType(ContentType.JSON)
                .body(requestBody)
                .when()
                .post("/process")
                .then()
                .statusCode(200)
                .body(equalTo("Order processed successfully"));
    }
}
