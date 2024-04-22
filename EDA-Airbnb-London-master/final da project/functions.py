import pandas as pd
def knn(latitude=0,longitude=0,place=0):
    df=pd.read_csv('pred2.csv')
    if(place!=0):
        df=df[df['neighbourhood']==place]
        return df['finl_income']
    if(latitude>51.70 or latitude<51.25 or longitude<-0.5 or longitude>0.27):
        return -1
    df=df[['finl_income','latitude','longitude']]
    df['calc']=(df['latitude']-latitude)**2+(df['longitude']-longitude)**2
    df=df.sort_values('calc')
    inc=list(df['finl_income'])
    inc[0]=inc[0]/2
    inc[1]=inc[1]/3
    inc[2]=inc[2]/6
    res=sum(inc[0:3])
    return res
def invest(amt):
    df=pd.read_csv('returns.csv')
    df1=df[df['Average']<=amt]
    df1=df1[df1['returns']<=30]
    df1=df1.sort_values('returns')
    print(df1[['Borough','Average','returns','total']])
