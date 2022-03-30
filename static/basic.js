function register(a, b) {
    $.ajax({
        type: "POST",
        url: "/register",
        dataType: 'json',
        headers: {
            // "Authorization": $.cookie('jwt-token')? 'Bearer ' + $.cookie('jwt-token') : null
            "Authorization": 'Bearer ' + $.cookie('jwt-token')
        },
        data: {
            time_give: a,
            type_give: b,
        },
        error: function(error) {
            alert('로그인 후 이용해주세요!');
            window.location.reload()
        },

        success: function(response) {
            if (response["result"] == "success") {
                $('#modal-comment').addClass('is-active')
            } else {
                alert("로그인 후 이용해주세요~!")
                window.location.reload()
            }
        }
    })
}

expired = () => alert("정원 초과입니다.")

function registerCmt(existCmt = true) {
  let cmt = ""
  if (existCmt) {
    cmt = $('#cmt').val()
    if (cmt == "") {
      alert("코멘트를 입력해주세요!")
      return null;
    }
  } else {
    cmt = "같이 운동해요!!"
  }
  $.ajax({
    type: "POST",
    url: "/register/comment",
    dataType: 'json',
    data: {
        comment: cmt
    },
    success: function(response) {
      if (response["result"] == "success") {
          alert("참가 완료!");
          window.location.reload()
      } else {
          alert("로그인 후 이용해주세요~!")
          window.location.reload()
      }
    }
  })
}

function logout() {
    $.ajax({
        type: 'GET',
        url: "/logout",
        headers: {
            "Authorization": 'Bearer ' + $.cookie('jwt-token')
        },
        success: function(response) {
            if (response["result"] == "success") {
                alert("로그아웃 완료!");
                location.href = "/";
            } else {
                alert(response['msg'])
            }
        }
    })
}

function remaindTime() {
  var now = new Date();
  var end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 24, 00, 00);
  var open = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 09, 00, 00);

  var nt = now.getTime();
  var et = end.getTime();
  var ot = open.getTime();
  if (nt < ot) {
      $('.time_text').fadeIn();
      $('button.reg_button').fadeOut();
      $("p.text_title").html('신청 시작까지 남은 시간');
      sec = parseInt(ot - nt) / 1000;
  } else {
      $('.time_text').fadeOut();
      $('button.reg_button').fadeIn();
      $("p.text_title").html('신청 마감까지 남은 시간');
      sec = parseInt(et - nt) / 1000;
  }
  day = parseInt(sec / 60 / 60 / 24);
  sec = (sec - (day * 60 * 60 * 24));
  hour = parseInt(sec / 60 / 60);
  sec = (sec - (hour * 60 * 60));
  min = parseInt(sec / 60);
  sec = parseInt(sec - (min * 60));
  if (hour < 10) {
      hour = "0" + hour;
  }
  if (min < 10) {
      min = "0" + min;
  }
  if (sec < 10) {
      sec = "0" + sec;
  }
  $(".hours").html(hour);
  $(".minutes").html(min);
  $(".seconds").html(sec);

}
setInterval(remaindTime, 1000);

document.addEventListener('DOMContentLoaded', () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    return null;
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);
    console.log($target);

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) { // Escape key
      closeAllModals();
    }
  });
});

$(document).ready(function(){
  $.ajax({
      url: 'https://api.openweathermap.org/data/2.5/weather?qSeoul&appid=f9d7a0fd2d6d72ccdcbd7efab92469e6&units=metric',
      dataType: 'json',
      type: 'GET',
      success: function(data){
          var $Icon = (data.weather[0].icon);
          var $Temp = Math.floor(data.main.temp) + '도';
          var $city = data.name;

           $('.CurrIcon').append('http://openweathermap.org/img/wn/' + $Icon + '@2x.png');
           $('.CurrTemp').prepend($Temp);
           $('.City').append($city);
      }
  })
});