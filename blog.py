from flask import Flask, render_template

app = Flask(__name__)

posts= [
        {
            'content':'This was revealed in a statement signed on Friday by the State House Director of Information', 
            'title': '1st Post', 
            'author': 'Adam',
            'date': '12/3/23'
            },
        {
            'content': 'Abiodun Oladunjoye, titled ‘President Tinubu appoints Gbajabiamila COS, Sen. Ibrahim Hadejia,',
              'title': '2nd Post',
                'author': 'Chris',
                  'date': '2/3/23'
                },
        {
            'content': ' Kaduna Speaker hails Gbajabiamila',
            'title': '3rd Post', 
            'author': 'Munir',
            'date': '1/5/23'
            }
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post')
def post():
    return render_template('post.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)