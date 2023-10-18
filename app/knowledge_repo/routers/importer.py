from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/knowledge_repo/importer",
    tags=["knowledge repo importer"],
)


@router.get("/")
async def root():
    return {'hello': 'world'}