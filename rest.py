from flask import Flask,request,jsonify
import sql
from bottelega import dict_cat,get_key
import newspik as na
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user', methods=['POST'])
def user():
    user_id = request.args.get('user_id')
    if(user_id == None):
        message = {"message":"Пустой аргумент с user_id"}
        return jsonify(message)
    else:
        if sql.check_sub(user_id):
            message = {"user_id":user_id,"message":"Данный пользователь уже подписан"}
            return jsonify(message)
        else:
            sql.add_sub(user_id)
            message = {"user_id":user_id,"message":"Данный пользователь был добавлен успешно"}
            return jsonify(message)

@app.route('/subscriptions/categories', methods=['GET','POST','DELETE'])
def cat():
    user_id = request.args.get('user_id')
    if request.method == 'GET':
        if(user_id == None):
            message = {"user_id":user_id,"message":"Пустой аргумент с user_id"}
            return jsonify(message)
        else:
            if sql.check_sub(user_id):
                if sql.check_cat(user_id):
                    message = {"user_id":user_id,"category":sql.ret_cat(user_id)}
                    return jsonify(message)
                else:
                    message = {"user_id":user_id,"message":"У данного пользователя нет категории"}
                    return jsonify(message)
            else:
                message = {"user_id":user_id,"message":"Данный пользователь не подписан"}  
                return jsonify(message)
    elif request.method == 'POST':
        cat = request.args.get('categories')
        if(user_id == None):
            message = {"user_id":user_id,"message":"Пустой аргумент с user_id"}
            return jsonify(message)
        else:
            if sql.check_sub(user_id):
                if sql.check_cat(user_id):
                    message = {"user_id":user_id,"message":"У данного пользавателя уже есть категория"}
                    return jsonify(message)
                else:
                    if cat in dict_cat.values():
                        sql.add_cat(user_id,cat)
                        message = {"user_id":user_id,"cat":cat,"message":"Категория была добавлена успешно"}
                        return jsonify(message)
                    else:
                        message = {"user_id":user_id,"cat":cat,"message":"Данной категории нет"}
                        return jsonify(message)

            else:
                message = {"user_id":user_id,"message":"Данный пользователь не подписан"}  
                return jsonify(message)
    elif request.method == 'DELETE':
        if(user_id == None):
            message = {"user_id":user_id,"message":"Пустой аргумент с user_id"}
            return jsonify(message)
        else:
            if sql.check_sub(user_id):
                if sql.check_cat(user_id):
                    sql.del_cat(user_id)
                    message = {"user_id":user_id,"message":"Категория была удалена успешно"}
                    return jsonify(message)
                else:
                    message = {"user_id":user_id,"message":"У данного пользователя нет категории"}
                    return jsonify(message)
            else:
                message = {"user_id":user_id,"message":"Данный пользователь не подписан"}  
                return jsonify(message)

@app.route('/subscriptions/keywords', methods=['GET','POST','DELETE'])
def kw():
    user_id = request.args.get('user_id')
    if request.method == 'GET':
        if(user_id == None):
            message = {"user_id":user_id,"message":"Пустой аргумент с user_id"}
            return jsonify(message)
        else:
            if sql.check_sub(user_id):
                if sql.check_kw(user_id):
                    message = {"user_id":user_id,"keywords":sql.ret_kw(user_id)}
                    return jsonify(message)
                else:
                    message = {"user_id":user_id,"message":"У данного пользователя нет ключевого слова"}
                    return jsonify(message)
            else:
                message = {"user_id":user_id,"message":"Данный пользователь не подписан"}  
                return jsonify(message)
    elif request.method == 'POST':
        kw = request.args.get('keywords')
        if(user_id == None):
            message = {"user_id":user_id,"message":"Пустой аргумент с user_id"}
            return jsonify(message)
        else:
            if sql.check_sub(user_id):
                if sql.check_kw(user_id):
                    message = {"user_id":user_id,"message":"У данного пользавателя уже есть ключевое слово"}
                    return jsonify(message)
                else:
                    sql.add_kw(user_id,kw)
                    message = {"user_id":user_id,"kw":kw,"message":"ключевое слово было добавлено успешно"}
                    return jsonify(message)

            else:
                message = {"user_id":user_id,"message":"Данный пользователь не подписан"}  
                return jsonify(message)
    elif request.method == 'DELETE':
        if(user_id == None):
            message = {"user_id":user_id,"message":"Пустой аргумент с user_id"}
            return jsonify(message)
        else:
            if sql.check_sub(user_id):
                if sql.check_kw(user_id):
                    sql.del_kw(user_id)
                    message = {"user_id":user_id,"message":"ключевое слово было удалено успешно"}
                    return jsonify(message)
                else:
                    message = {"user_id":user_id,"message":"У данного пользователя нет ключевого слова"}
                    return jsonify(message)
            else:
                message = {"user_id":user_id,"message":"Данный пользователь не подписан"}  
                return jsonify(message)
    
@app.route('/news', methods=['GET'])
def news():
    user_id = request.args.get('user_id')
    if(user_id == None):
        message = {"message":"Пустой аргумент с user_id"}
        return jsonify(message)
    else:
        if sql.check_sub(user_id):
            d_news={}
            if(not sql.check_cat(user_id) and not sql.check_kw(user_id)):
                for i,j in zip(na.ret_news(),na.ret_news_url()):
                    d_news[i]=j
            elif(sql.check_cat(user_id) and not sql.check_kw(user_id)):
                for i,j in zip(na.ret_news(cat=sql.ret_cat(user_id)),na.ret_news_url(cat=sql.ret_cat(user_id))):
                    d_news[i]=j
            elif(not sql.check_cat(user_id) and sql.check_kw(user_id)):
                for i,j in zip(na.ret_news(kw=sql.ret_kw(user_id)),na.ret_news_url(kw=sql.ret_kw(user_id))):
                    d_news[i]=j
            else:
                for i,j in zip(na.ret_news(kw=sql.ret_kw(user_id),cat=sql.ret_cat(user_id)),na.ret_news_url(kw=sql.ret_kw(user_id),cat=sql.ret_cat(user_id))):
                    d_news[i]=j

            message = {"news":d_news}
            return jsonify(message)
        else:
            sql.add_sub(user_id)
            message = {"user_id":user_id,"message":"Данный пользователь не подписан"}
            return jsonify(message)


if __name__ == "__main__":
    app.run()