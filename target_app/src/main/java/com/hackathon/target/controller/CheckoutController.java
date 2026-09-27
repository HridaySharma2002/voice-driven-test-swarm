package com.hackathon.target.controller;

import com.hackathon.target.model.OrderRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/checkout")
public class CheckoutController {

    @PostMapping("/process")
    public ResponseEntity<String> processOrder(@RequestBody OrderRequest order) {
        // DELIBERATE BUG: Hardcoded error. Test expects 90.0 for $100 item with 10% discount.
        double finalPrice = order.getPrice() - order.getDiscount();

        if (finalPrice != 90.0) {
            return ResponseEntity.badRequest().body("Price calculation failed. Expected 90.0, got " + finalPrice);
        }

        return ResponseEntity.ok("Order processed successfully");
    }
}
