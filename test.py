from turtle import xcor
from utils.init_db import *

db.user.drop()




<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Mini Project</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"
    />
    <script
      src="https://code.jquery.com/jquery-3.6.0.js"
      integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk="
      crossorigin="anonymous"
    ></script>
    <script src="../static/jquery.cookie.js"></script>

    <style>
      .wrap {
        margin: auto;
        width: 1000px;
      }

      table {
        width: 800px;
        height: 300px;
      }

      table.center {
        margin-left: auto;
        margin-right: auto;
      }

      img{
        width: auto;
        height: 300px;
      }
    </style>
    <script>
      function logout() {
        $.ajax({
          type: "GET",
          url: "/logout",
          headers: {
            Authorization: "Bearer " + $.cookie("jwt-token"),
          },
          success: function (response) {
            if (response["result"] == "success") {
              alert("로그아웃 완료!");
              location.href = "/";
            } else {
              alert("로그아웃 실패!");
            }
          },
        });
      }

      var imgurl="/static/images/" + '{{result["type"]}}' + ".png";
      window.onload = function(){
        document.getElementById("imageid").src = imgurl;
      }

    </script>
  </head>

  <body>
    <div class="wrap pt-5">
      {% if loginChecked %}
      <div class="buttons is-right pt-3">
        <a class="button is-success" href="login">로그인</a>
        <a class="button is-light" href="signup">회원가입</a>
      </div>
      {% else %}
      <div class="buttons is-right pt-3">
        {{username}}님 환영합니다.
        <button class="button is-success ml-3" onclick="logout()">
          로그아웃
        </button>
      </div>
      {% endif %}

      <div class="has-text-centered pb-6">
        <h1 class="title box has-background-success has-text-white">
          정글 운동 매칭 서비스
        </h1>
      </div>

      <div class="has-text-centered">
        <h1 class="title">매칭 결과</h1>
      </div>

      {% if (result['players']|length)>=2 %} {% set _dummy=result['players'].remove(username) %}

        <div class="has-text-centered pt-6">
            <!-- <p class="title pb-5">{{username}}님</p>  -->
            <p class="subtitle">{% for player in result['players'][:-1]%}
                <strong>{{player}}</strong>님, {% endfor %}
                <strong>{{result['players'][-1]}}</strong>님과 함께 <strong>{{result["type"]}}</strong>입니다.</p>
            <p class="subtitle">시간 : 아침 <strong>{{result['time'].split(':')[0][1]}}</strong>시</p>
            <p class="subtitle">장소 : {%if (result["type"] == 헬스)%} 강의동 지하 1층 헬스장 {%else%} 기숙사 앞{%endif%}</p>
            <img id="imageid" src="">
        </div>
        {%else%}
        <div class="has-text-centered pt-6">
            <!-- <p class="title pb-5">{{username}}님</p>  -->
            <p class="subtitle">인원 미달로 매칭이 성사되지 않았습니다.</p>
            <img src="/static/images/fail.png"> {% endif %}

        </div>

        <div class="has-text-centered">
           <script> 
            {% set h_list = [] %} {% set w_list = [] %} {% set r_list = [] %} {% for k, v in userlog.items() %} {%if v == '헬스' %} {{h_list.append(k)}} {% elif v == '산책' %} {{w_list.append(k)}} {% else %} {{r_list.append(k)}} {% endif %} {% endfor %}
            </script>
            <p class="title">운동 기록</p>
            <p>헬스 횟수 : {{h_list|length}}, 운동한 날 : {% for day in h_list %}<span>{{day[:4]}}년{{day[4:6]}}월{{day[6:]}}일   </span>{%endfor%}</p>
            <p>산책 횟수 : {{w_list|length}}, 운동한 날 : {% for day in w_list %}<span>{{day[:4]}}년{{day[4:6]}}월{{day[6:]}}일   </span>{%endfor%}</p>
            <p>러닝 횟수 : {{r_list|length}}, 운동한 날 : {% for day in r_list %}<span>{{day[:4]}}년{{day[4:6]}}월{{day[6:]}}일   </span>{%endfor%}</p>
        </div>

        <p class="title pt-6 has-text-centered">운동 랭킹</p>
<table class="table center has-text-centered">

    {{count_data[0]['health_count'] + count_data[0]['walking_count'] + count_data[0]['running_count']}}
    <thead>
        <th>헬스</th>
        <th>산책</th>
        <th>러닝</th>
        <th>종합</th>
    </thead>
    <tbody>
        <th>
            {% for user in count_data|sort(attribute="health_count", reverse=True) %}
            <p>{{user['username']}} : {{user['health_count']}}회</p> 
            {% endfor %} 
        </th>
        <th>
            {% for user in count_data|sort(attribute="walking_count", reverse=True) %}
            <p>{{user['username']}} : {{user['walking_count']}}회</p> 
            {% endfor %} 
        </th>
        <th>
            {% for user in count_data|sort(attribute="running_count", reverse=True) %}
            <p>{{user['username']}} : {{user['running_count']}}회</p> 
            {% endfor %} 
        </th>
        <th>
            {% for user in count_data|sort(attribute="", reverse=True) %}
            <p>{{user['username']}} : {{user['total_count']}}회</p> 
            {% endfor %} 
        </th>
    </tbody>
</table>

</body>

</html>