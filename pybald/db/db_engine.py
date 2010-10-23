import sqlalchemy as sa
import project

engine_args = project.get_engine_args()

if project.green:
    from SAGreen import green_connection, GreenThreadQueuePool
    engine_args["creator"] = green_connection()
    engine_args["poolclass"] = GreenThreadQueuePool

engine = sa.create_engine(project.get_engine(), **engine_args)