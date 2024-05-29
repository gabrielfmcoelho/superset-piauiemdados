from fastapi import APIRouter
from contextlib import contextmanager
from icecream import ic
from datetime import datetime as dt
from datetime import timedelta


from database.connector import Connector
from schemas.dashboard import DashboardFilters, Filter, Indicator
from models.active_companies import ActiveCompany, ActiveCompanyActivities
from models.opening_companies import OpeningCompany, OpeningCompanyActivities, OpeningCompanyTimeSeries


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@contextmanager
def get_db_session():
    SessionLocal = Connector.get_instance().get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_filters(opening_filters: DashboardFilters, filter_name: str | None = None) -> dict:
    _ = {k: v for k, v in opening_filters.dict().items() if v is not None}
    if filter_name:
        _.pop(filter_name, None)
    return _

@router.get(
    "/filters/{filter_name}",
    response_model=Filter,
)
async def get_filter(
    filter_name: str,
    opening_filters: DashboardFilters = DashboardFilters()
) -> Filter:
    ic("Getting filters")
    with get_db_session() as db:
        filters = parse_filters(opening_filters, filter_name)
        print(filters)
        # get available values for each filter given its context
        # if no context is given, return all available values
        # OpeningCompany + OpeningCompanyActivities
        values = set()
        if filter_name == "year":
            query = db.query(OpeningCompany.year)
        elif filter_name == "nature_type_descr":
            query = db.query(OpeningCompany.nature_type_descr)
        elif filter_name == "city":
            query = db.query(OpeningCompany.city)

        if filters != {} and filters != None:
            if "year" in filters:
                query = query.filter_by(year=filters["year"])
            if "nature_type_descr" in filters:
                query = query.filter_by(nature_type_descr=filters["nature_type_descr"])
            if "city" in filters:
                query = query.filter_by(city=filters["city"])

        available_values = query.distinct().all()
        for value in available_values:
            values.add(value[0])

        if len(values) == 0:
            values = None  

        return Filter(values=values)
    
@router.get(
    "/filters",
    response_model=DashboardFilters,
)
async def get_all_filters(
    opening_filters: DashboardFilters = DashboardFilters()
) -> DashboardFilters:
    ic("Getting all filters")
    with get_db_session() as db:
        years = await get_filter("year", opening_filters)
        nature_type_descrs = await get_filter("nature_type_descr", opening_filters)
        cities = await get_filter("city", opening_filters)
        return DashboardFilters(
            year=years,
            nature_type_descr=nature_type_descrs,
            city=cities
        )

@router.get(
    "/indicator/{indicator_id}",
)
async def get_chart(
    indicator_id: int,
    opening_filters: DashboardFilters
):
    ic("Getting chart")
    with get_db_session() as db:
        filters = parse_filters(opening_filters)
        if indicator_id == 1:
            query = db.query(OpeningCompany.hash_key)
            if filters != {} and filters != None:
                query = query.filter_by(**filters)
            indicator = query.distinct().count()
        elif indicator_id == 2:
            query = db.query(OpeningCompanyActivities.hash_key)
            if filters != {} and filters != None:
                query = query.filter_by(**filters)
            indicator = query.distinct().count()
        elif indicator_id == 3:
            query = db.query(OpeningCompanyTimeSeries.register_hours_duration)
            if filters != {} and filters != None:
                query = query.filter_by(**filters)
            query_result = query.all()
            # values are in format "00:00:00" hh:mm:ss transform to seconds and get the average
            for value in query_result:
                # transform "00:00:00" hh:mm:ss transform to second and get the avaerage in hours
                indicator = sum([int(v.split(":")[0]) * 3600 + int(v.split(":")[1]) * 60 + int(v.split(":")[2]) for v in query_result]) / len(query_result)
                indicator = round(indicator / 3600, 2)
        return Indicator(value=str(indicator))

