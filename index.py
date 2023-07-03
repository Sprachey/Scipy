from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio


app = Flask(__name__)
app.debug = True

df = pd.read_csv('data/QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
df.DATE = pd.to_datetime(df.DATE)
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
reshaped_df.drop_duplicates()
reshaped_df.fillna(0, inplace=True) 
stats=reshaped_df.describe()
col=reshaped_df.columns.to_series()

roll_df = reshaped_df.rolling(window=6).mean()
pop=reshaped_df.loc[:,:].max()

plt.figure(figsize=(16,10))
plt.grid(color="grey")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column], 
             linewidth=3, label=roll_df[column].name)
plt.legend(fontsize=16)

for r in col:
    plt.figure(figsize=(16,10))
    plt.grid(color="grey")
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Number of Posts', fontsize=20)
    plt.ylim(0, 35000)
    nam=col[r]
    plt.title(f"{nam}",fontsize=24)
    plt.scatter(reshaped_df.index, reshaped_df[f"{nam}"],label=nam)
    # plt.savefig(f"{nam}.png")

@app.route('/')
def home():
    fig=px.bar(x=pop.index,y=pop.values,hover_name=pop.index,
           title="Popularity of Programming Languages"  ,
           color=pop.index,
           color_continuous_scale="Agsunset")
    fig.update_layout(xaxis_title="Programming Languages",
                  yaxis_title="Number of Posts",
                  coloraxis_showscale=False
                  )
    
    graph_jsonbr=pio.to_json(fig)
    return render_template('layouts/index.html',data_rev=reshaped_df.sample(10).to_html(),graph_jsonbr=graph_jsonbr)

@app.route('/stats')
def basic_stats():
    
    return render_template('layouts/statistics.html',stats_table=stats.to_html())

@app.route('/data')
def used_data():

    return render_template('layouts/UsedData.html',data_table=reshaped_df.to_html())

@app.route('/graphs')
def graph():
    fig=px.scatter(data_frame=pop,x=pop.index,y=pop.values,
               title='Popularity of Programming Languages',
               hover_name=pop.index,
               color=pop.index)
    fig.update_layout(xaxis_title="Programming Languages",
                      yaxis_title="Number of Posts")
    graph_jsonsc=pio.to_json(fig)
    return render_template('layouts/Graph.html',graph_jsonsc=graph_jsonsc)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
