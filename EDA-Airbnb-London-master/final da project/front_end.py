import streamlit as st 
from PIL import Image 
# EDA Pkgs
import pandas as pd 
import numpy as np 

# Data Viz Pkg
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns

data = ("listings.csv")

st.markdown("# Estimation of AirBnB property investment as a Profitable Marwari Business")
st.text('London airbnb dataset is loaded!')
st.markdown("Find out what rental you could earn "
            "This web app lets you know the **expected annual income** after tax you'll be earning in **AirBnB** properties in **UK!**")
df = pd.read_csv(data)
pred = pd.read_csv(("pred2.csv"))
ins=pd.read_excel(('investment.xlsx'))
ins['total']=pred['total']
ins['finl_income']=pred['finl_income']
ins['returns']=ins['Average']/ins['finl_income']

st.sidebar.subheader(' Quick  Explore')
st.sidebar.text("Tick the box to explore the dataset.")
#if st.checkbox("Show Raw Data", False):
if st.sidebar.checkbox('Raw Data'):
    st.subheader('Raw data')
    st.write(df.head())
    st.text('The number of rows and columns in the dataset is:')
    st.write(df.shape)

if st.sidebar.checkbox('Missing Values?'):
        st.subheader('Missing values')
        st.write(df.isnull().sum())
df=df.drop(['neighbourhood_group'],axis=1)   
df.drop_duplicates(subset=None, keep="first", inplace=True)
         
if st.sidebar.checkbox('Statistical Description'):
        st.subheader('Statistical Data Descripition')
        st.write(df.describe())

def groups(df,cname,rename,rn=0,p=0):
    dummy_df=df.groupby(cname).id.count().sort_values(ascending=False)
    dummy_df = dummy_df.reset_index()
    if(rn):
        dummy_df.rename(columns={rename[0]:rename[1]}, inplace=True)
    if(p):
        dummy_df["percentage"]=round(dummy_df["count"] / dummy_df["count"].sum()*100,2)
    return dummy_df
def plotdata(df,X,Y,X_title,Y_title):
    #plt.figure(figsize=(5,5)),
    plt.style.use('default')
    ax = sns.barplot(x=X, y=Y, data=df)
    plt.title("Disturibution", weight="bold", c="red", fontsize=15)
    plt.xlabel(X_title,weight="bold",c="k")
    plt.xticks(rotation=90, weight="bold")
    plt.ylabel(Y_title,weight= "bold",c="k")
    plt.yticks(weight="bold")
    #for p in ax.patches:
    #        ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.4, p.get_height()),
    #                    ha='center', va='bottom',
    #                    color= 'black')
    plt.show()
st.set_option('deprecation.showPyplotGlobalUse', False)

listing1=df[df['price']>=35]
listing1=listing1[listing1['price']<=150]
listing1['annual_income']=listing1['price']*(365-listing1['availability_365'])
inc=listing1.groupby('neighbourhood').sum().reset_index()
mark=listing1.groupby('neighbourhood').mean().reset_index()
inc['longitude']=mark['longitude']
inc['latitude']=mark['latitude']

def knn(df,latitude=0,longitude=0,place=0):
    #df=pd.read_csv('pred2.csv')
    if(place!=0):
        df=df[df['neighbourhood']==place]
        return df['finl_income']
    if(latitude>51.70 or latitude<51.25 or longitude<-0.5 or longitude>0.27):
        return -1
    df=df[['finl_income','latitude','longitude']]
    df['latitude']=np.deg2rad(df['latitude'])
    df['longitude']=np.deg2rad(df['longitude'])
    latitude=latitude*22/(180*7)
    longitude=longitude*22/(180*7)
    df['nlati']=df['latitude']-latitude
    df['nlongi']=df['longitude']-longitude
    df['p1']=np.power(np.sin(df['nlati']/2),2)+np.cos(df['nlati'])*np.cos(df['nlongi'])*np.power(np.sin(df['nlongi']/2),2)
    df['calc']=np.arcsin(np.sqrt(df['p1']))*2
    df['calc']=df['calc']+0.00001
    df['calc']=1/df['calc']
    df=df.sort_values('calc')
    df['calc2']=df['calc']*df['finl_income']
    inc=list(df['calc2'])
    inc1=list(df['calc'])
    res=sum(inc[-3:])/sum(inc1[-3:])
    return res

def invest(ins, amt):
    ins1=ins[ins['Average']<=amt]
    ins1=ins1[ins1['returns']<=30]
    ins1=ins1.sort_values('returns')
    return ins1[['Borough','Average','returns','total']]

if st.sidebar.checkbox('Data grouped by neighbourhood'):     
    inc
    inc.shape
    
if st.sidebar.checkbox('Visualization'):    
    option = st.selectbox('Select the visual representation',('None','Type_of_room v/s Number_of_rooms', 
                                                              'Neighbourhood v/s Number_of_rooms', 
                                                              'Neighbourhood v/s Average_price',
                                                              'Neighbourhood v/s Availability_365',
                                                              "Neighbourhood v/s No_of_days_occupied",
                                                              'Airbnb Properties by Price/Night',
                                                              'Airbnb Properties availability throughout the year',
                                                              'Airbnb Properties by Annual Income',
                                                              'Airbnb Properties by Total Income per Neighourhood',
                                                              'Annual Income per property of a specific neighbourhood',
                                                              'Time to get back investment(in years)'))
    st.write('You selected:', option)
    if(option == "Type_of_room v/s Number_of_rooms"):
        room_data=groups(df,'room_type',['id','count'],1,1)
        fig = plotdata(room_data,'room_type','count', "Type_of_room", "Number_of_rooms")
        st.pyplot(fig)
    if(option == "Neighbourhood v/s Number_of_rooms"):
        neighnourhood_data=groups(df,'neighbourhood',['id','count'],1,1)
        fig = plotdata(neighnourhood_data,'neighbourhood','count',"Neighbourhood", "Number_of_rooms")
        st.pyplot(fig)
        
    if(option == "Neighbourhood v/s Average_price"):    
        neigh_price = df.groupby("neighbourhood").price.mean().sort_values(ascending=False)
        neigh_price = neigh_price.reset_index()
        fig = plotdata(neigh_price,'neighbourhood','price',"Neighbourhood", "Average_price")     
        st.pyplot(fig)
    
    if(option == "Neighbourhood v/s Availability_365"):    
        occupancy_borough = df.groupby("neighbourhood").availability_365.mean().sort_values().reset_index()
        fig = plotdata(occupancy_borough,"neighbourhood",'availability_365',"Neighbourhood","Availability_365")    
        st.pyplot(fig)
    
    if(option == "Neighbourhood v/s No_of_days_occupied"):
        occupancy_borough = df.groupby("neighbourhood").availability_365.mean().sort_values().reset_index()
        occupancy_borough['tourists']=365-occupancy_borough.availability_365
        fig = plotdata(occupancy_borough,"neighbourhood",'tourists',"Neighbourhood","No_of_days_occupied")
        st.pyplot(fig)
        
    if(option == "Airbnb Properties by Price/Night"):
        plt.figure(figsize=(15,10),dpi=200)
        listing_map=listing1.plot(kind='scatter', x='longitude', y='latitude', c='price', cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4,figsize=(15,10))
        plt.title("Airbnb Properties by Price/Night")
        fig = plt.show()
        st.pyplot(fig)
    
    if(option == "Airbnb Properties availability throughout the year"):
        plt.figure(figsize=(15,10),dpi=200)
        listing_map=listing1.plot(kind='scatter', x='longitude', y='latitude', c='availability_365', cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4,figsize=(15,10))
        plt.title("Airbnb Properties by Availability/Night")
        fig = plt.show()
        st.pyplot(fig)
    if(option == "Airbnb Properties by Annual Income"):
        plt.figure(figsize=(15,10),dpi=200)
        listing_map=listing1.plot(kind='scatter', x='longitude', y='latitude', c='annual_income', cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4,figsize=(15,10))
        plt.title("Airbnb Properties by Annual Income")
        fig = plt.show()
        st.pyplot(fig)

    if(option == "Airbnb Properties by Total Income per Neighourhood"):
        plt.figure(figsize=(15,10),dpi=200)
        listing_map=inc.plot(kind='scatter', x='longitude', y='latitude', c='annual_income', cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4,figsize=(15,10))
        plt.title("Airbnb Properties by Total Income per Neighourhood")
        fig = plt.show()
        st.pyplot(fig)


    if(option == "Annual Income per property of a specific neighbourhood"):
        plt.figure(figsize=(15,10),dpi=200)
        listing_map=pred.plot(kind='scatter', x='longitude', y='latitude', c='annual_income', cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4,figsize=(15,10))
        plt.title("Annual Income per property of a specific neighbourhood")
        fig = plt.show()
        st.pyplot(fig)

    if(option == 'Time to get back investment(in years)'):
        plt.figure(figsize=(15,10),dpi=200)
        listing_map=ins.plot(kind='scatter', x='longitude', y='latitude', c='returns', cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4,figsize=(15,10))
        plt.title("Time to get back investment(in years)")
        fig = plt.show()
        st.pyplot(fig)

if st.sidebar.checkbox('Rental you could earn'):
    st.text("Lets you know the expected annual income after tax deduction that you'll earn")
    # img=Image.open('C:\\Users\\cheri\\Desktop\\CHERI\\College\\SEM -V\\Airbnb_London\\london-boroughs-map.jpg')
    # st.image(img,width=500)
    if st.checkbox('Based on neighbourhood'):
        place1 = st.selectbox('Select the neighbourhood', pred['neighbourhood'])
        final = knn(pred, place = place1)
        st.write(final)
    if st.checkbox('Based on latitude and longitude'):
        lat1 = st.number_input('Insert latitude', min_value = 51.25, max_value = 51.70)
        longt1 = st.number_input('Insert longitude', min_value = -0.5, max_value = 0.27)
        st.write('The latitude is ', lat1)
        st.write('The longitude is ', longt1)
        res = knn(pred, latitude = lat1, longitude = longt1)
        st.write(res)
        
if st.sidebar.checkbox('Neighbourhoods to invest based on investment amount'):
    inv_amount = st.number_input("Insert the investment amount", min_value = 300000)
    st.write("The investment is", inv_amount)
    table = invest(ins, amt = inv_amount)
    table
    st.text("The number of neighbourhood options available is ")
    st.text(len(table)) 
    
