WORKERS := 1

.PHONY: all
all:
	@git pull
	@sleep 25
	@luigi --module pipeline FDCPipeline --workers $(WORKERS)
