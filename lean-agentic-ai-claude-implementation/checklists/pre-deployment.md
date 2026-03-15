# Pre-Deployment Checklist
- [ ] Agent count justified (3-gate test)
- [ ] Models right-sized per agent
- [ ] Tools scoped per agent (no "give all")
- [ ] Reflection is conditional
- [ ] RAG is gated
- [ ] Cost budget per request defined
- [ ] Turn/iteration limits set
- [ ] Cost monitoring with alerts
- [ ] Deployment region selected for carbon
- [ ] Memory has TTLs
- [ ] Response caching implemented
- [ ] Human escalation paths defined
- [ ] Circuit breakers on failures
- [ ] Audit logging in place
- [ ] Output validation before delivery
Below 70% checked = significant risk. Below 50% = do not deploy.
