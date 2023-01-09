from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..deps import get_current_user
from ..core.schemas.schemas import Post, UpdatePost
from ..core.models import models
from ..core.models.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", summary='Create new post')
def create_post(data: Post, db: Session = Depends(get_db), user: models.Users = Depends(get_current_user)):
    post = db.query(models.Users).filter_by(email=data.title).first()
    if post is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    post_model = models.Posts()
    post_model.title = data.title
    post_model.content = data.content
    post_model.author_id = user.id

    db.add(post_model)
    db.commit()
    return JSONResponse(
        content={},
        headers={"Location": "/posts/"+str(post_model.id)},
        status_code=status.HTTP_201_CREATED
    )


@router.put("/edit")
def edit_post(post_id: int, update: UpdatePost, db: Session = Depends(get_db), user: models.Users = Depends(get_current_user)):
    post = db.query(models.Posts).get(post_id)
    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot edit other user's posts"
        )
    if update.title:
        post.title = update.title
    if update.content:
        post.content = update.content
    db.commit()
    return JSONResponse(
        content={},
        status_code=status.HTTP_200_OK
    )


@router.put("/react/{post_id}", summary="React to post")
def post_react(post_id: int, reaction: str, db: Session = Depends(get_db), user: models.Users = Depends(get_current_user)):
    post = db.query(models.Posts).get(post_id)
    if post.author_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot react to user's own post"
        )
    if reaction not in ["like", "dislike"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown reaction"
        )
    print(db.query(models.PostReactions).filter_by(post_id=post_id, user_id=user.id, reaction=reaction))
    if db.query(models.PostReactions).filter_by(post_id=post_id, user_id=user.id, reaction=reaction).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot react twice"
        )
    old_reaction = db.query(models.PostReactions).filter_by(post_id=post_id, user_id=user.id).first()
    if old_reaction is not None:
        db.delete(old_reaction)
    reaction_model = models.PostReactions()
    reaction_model.post_id = post_id
    reaction_model.user_id = user.id
    reaction_model.reaction = reaction
    db.add(reaction_model)
    db.commit()

    return JSONResponse(
        content={},
        status_code=status.HTTP_200_OK
    )




@router.delete("/{post_id}")
def del_post(post_id: int, db: Session = Depends(get_db), user: models.Users = Depends(get_current_user)):
    inst = db.get(models.Posts, post_id)
    if inst.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other user's posts"
        )
    db.delete(inst)
    db.commit()
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.get("/")
def get_posts(limit: int, offset: int, db: Session = Depends(get_db)):
    posts = db.query(models.Posts).offset(offset=offset).limit(limit=limit).all()
    return posts


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).get(post_id)
    likes = db.query(models.PostReactions).filter_by(post_id=post_id, reaction="like").count()
    dislikes = db.query(models.PostReactions).filter_by(post_id=post_id, reaction="dislike").count()
    return {
            "post": post,
            "likes": likes,
            "dislikes": dislikes
        }
