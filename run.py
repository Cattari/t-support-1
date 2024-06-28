if __name__ == "__main__":
    import uvicorn
    from settings import PORT
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
