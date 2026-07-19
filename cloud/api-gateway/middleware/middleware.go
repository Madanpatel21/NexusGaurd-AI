package middleware

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

// Auth returns a middleware that validates the incoming Bearer token.
func Auth() gin.HandlerFunc {
	return func(c *gin.Context) {
		token := c.GetHeader("Authorization")
		if token == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing authorization header"})
			return
		}
		// In production: validate JWT against Vault/Istio-issued principal.
		c.Next()
	}
}

// RateLimit is a simple in-memory token-bucket rate limiter.
func RateLimit() gin.HandlerFunc {
	type bucket struct {
		mu       sync.Mutex
		tokens   float64
		last     time.Time
		max      float64
		rate     float64 // tokens per second
	}

	const maxTokens = 100
	const refillRate = 20.0

	buckets := make(map[string]*bucket)
	var bm sync.Mutex

	getBucket := func(key string) *bucket {
		bm.Lock()
		defer bm.Unlock()
		b, ok := buckets[key]
		if !ok {
			b = &bucket{tokens: maxTokens, last: time.Now(), max: maxTokens, rate: refillRate}
			buckets[key] = b
		}
		return b
	}

	return func(c *gin.Context) {
		key := c.ClientIP()
		b := getBucket(key)

		b.mu.Lock()
		defer b.mu.Unlock()

		now := time.Now()
		elapsed := now.Sub(b.last).Seconds()
		b.tokens += elapsed * b.rate
		if b.tokens > b.max {
			b.tokens = b.max
		}
		b.last = now

		if b.tokens < 1 {
			c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"error": "rate limit exceeded"})
			return
		}
		b.tokens -= 1
		c.Next()
	}
}
