
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager,jwt_required,create_access_token

from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta


app=Flask(__name__)

#add configuration


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:002@localhost/guvi' #guvi is database has to be created earlier

app.config['SECRET_KEY'] = 'ishwarya@0110'

db = SQLAlchemy(app)
jwt=JWTManager(app)
#database models
#using db.Model to create the class
class Engagement(db.Model):
    #define fields for table
    __tablename__="Engagement"
    EngagementId=db.Column(db.Integer,primary_key=True,autoincrement=False)
    GlobalId=db.Column(db.String(100))
    Month=db.Column(db.String(10))
    Year=db.Column(db.Integer)
    EWSCategory=db.Column(db.String(10),nullable=False)
    BusinessImpact=db.Column(db.String(10),nullable=False)
    Reason=db.Column(db.String(100),nullable=False)
    DetailSeason=db.Column(db.String(1000),nullable=False)
    ProposedAction=db.Column(db.String(1000),nullable=False)
    TimeLine=db.Column(db.DateTime,nullable=False)
    CreatedDate=db.Column(db.DateTime)
    CreatedBy=db.Column(db.String(50))
    UpdatedDate=db.Column(db.DateTime)
    UpdatedBy=db.Column(db.String(50))
 

@app.route("/login",methods=['POST'])
def login():
    
    if request.is_json:
       username=request.json["username"]
       password=request.json["password"]
    else:
       username=request.form["username"]
       password=request.form["password"]
    
    #test=User.query.filter_by(user=username,password=password)
    test=False
    if(username=="Abc" and password=="123"):
        test=True

    if test:
        #create access token
        expiry=timedelta(hours=1)
        access_token=create_access_token(identity=username,expires_delta=expiry)
        return jsonify(message="Login_succeded",access_token=access_token,access_token_expiry=str(expiry))
    else:
        return jsonify(message="no user exists")


@app.route('/add_record',methods=['POST'])
@jwt_required()
def add_records():
    current_user = get_jwt_identity()


    engagement_id=request.get_json()["EngagementId"]
    check=Engagement.query.filter_by(EngagementId=engagement_id).first()
    if check:
        return jsonify(message="The record already exists")
    else:
        Global_Id=request.get_json()["GlobalId"]
        month=request.get_json()["Month"]
        year=request.get_json()["Year"]
        EWS_category=request.get_json()["EWSCategory"]
        Business_Impact=request.get_json()["BusinessImpact"]
        Var_reason=request.get_json()["Reason"]
        Detail_Season=request.get_json()["DetailSeason"]
        Proposed_Action=request.get_json()["ProposedAction"]
        Time_line=request.get_json()["TimeLine"]
        created_Date=datetime.now()
        updated_Date=created_Date
        created_By=current_user
        updated_By=current_user
        new_user=Engagement(EngagementId=engagement_id,GlobalId=Global_Id,Month=month,Year=year
        ,EWSCategory=EWS_category,BusinessImpact=Business_Impact,Reason=Var_reason,DetailSeason=Detail_Season,
        ProposedAction=Proposed_Action,TimeLine=Time_line,
        CreatedDate=created_Date,UpdatedDate=updated_Date,CreatedBy=created_By,UpdatedBy=updated_By)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="added new user")


@app.route("/update_records",methods=['PUT'])
@jwt_required()
def update_record():
    current_user = get_jwt_identity()
    Engagement_ID=request.get_json()["EngagementId"]
    old_user=Engagement.query.filter_by(EngagementId=Engagement_ID).first()
    data=request.get_json()
    if old_user:
        if("EWSCategory" in data):
            old_user.EWSCategory=request.get_json()["EWSCategory"]
            
        if("BusinessImpact" in data):
            old_user.BusinessImpact=request.get_json()["BusinessImpact"]
       
        if("Reason" in data):
            old_user.Reason=request.get_json()["Reason"]
            
        
        if("DetailSeason" in data):
            old_user.DetailSeason=request.get_json()["DetailSeason"]
            
        if("ProposedAction" in data):
            old_user.ProposedAction=request.get_json()["ProposedAction"]
        
        if("TimeLine" in data):
            old_user.TimeLine=request.get_json()["TimeLine"]
           
        
        Updated_date=datetime.now()

        old_user.UpdatedDate=Updated_date
        old_user.UpdatedBy=current_user
        db.session.commit()
      
        return jsonify(message="Update successful")
    else:
        return jsonify(message="No existing record")


def db_drop():
    db.drop_all()


def db_create():
    db.create_all()
    

if __name__=="__main__":
    #db_drop()
    db_create()
    app.run(debug=True)



