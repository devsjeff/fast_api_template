# One-Line Explanation:   
# Depends() runs a function BEFORE your route, and passes its return value to your route. If the dependency raises an error, your route never runs.

from fastapi import Depends, HTTPException , FastAPI
app = FastAPI()

# Dependency function
def get_user():
    user = db.query(User).first()
    if not user:
        raise HTTPException(401)  # Stops route
    return user  # Passed to route

# Route using dependency
@app.get("/profile")
def profile(user = Depends(get_user)):  # Runs get_user() first
    return {"user": user}  # Only runs if get_user() succeeded




#1. Request comes in  
# 2. FastAPI runs get_user()
# 3. Success? → return user → run profile()  
# 4. Fail? → raise error → profile() NEVER runs
