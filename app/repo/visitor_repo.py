from datetime import datetime
from sqlalchemy.sql import func
from typing import Generic
from app.models.visitiors_models import Visits
from app.schema.visits_schemas import CreateVisits


class VisitorRepositories():
    
    def get_by_ip(db,ip:str):
        return db.query(Visits).filter(Visits.visit_ip_address == ip).first()

    def create_visit(db, obj_in:str):
        db_obj=Visits(visit_ip_address=obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def check_ip_limit(db, ip:CreateVisits):
        is_limit_exceeded = db.query(Visits).filter(Visits.visit_ip_address == ip and func.to_char(Visits.created_at("%Y-%m-%d")) == datetime.now().strftime("%Y-%m-%d")).count()
        

        if is_limit_exceeded < 3:
            return False
        else:
            return True



visitor_repo = VisitorRepositories



#   created_at_date = datetime.strptime(created, 
#                                  "%d%b%Y%H%M%S")