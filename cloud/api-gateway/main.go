package main

import (
	"github.com/gin-gonic/gin"
	"nexusguard/middleware"
)

func main() {
	r := gin.Default()
	r.Use(middleware.Auth())
	r.Use(middleware.RateLimit())
	
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})
	
	r.Run(":8080")
}
