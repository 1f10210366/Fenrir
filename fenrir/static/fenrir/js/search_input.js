let API_KEY_HOTPEPPER = '7699907c06980421';
let API_KEY_Google = 'AIzaSyBhg8RBbcrfWT_R3E2dISbpqHtSC7LLUwY';

let map;
let currentPosition;  

// ページがロードされたときに getCurrentLocation 関数を呼び出す
document.addEventListener('DOMContentLoaded', function () {
  getCurrentLocation();
});

//現在地情報の取得
function getCurrentLocation() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
          function (position) {
              currentPosition = { lat: position.coords.latitude, lng: position.coords.longitude };
              document.getElementById('latitude').value = position.coords.latitude;
              document.getElementById('longitude').value = position.coords.longitude;
              initMap();  // getCurrentLocation の中で位置情報を取得したら initMap を呼び出す
          },
          function (error) {
              console.error('位置情報の取得に失敗しました', error);
          }
      );
  } else {
      console.error('Geolocationがサポートされていません');
  }
}


//地図の表示
function initMap() {
    // Google Mapを初期化
    map = new google.maps.Map(document.getElementById('map'), {
        center: currentPosition,
        zoom: 15
    });

    // 現在地にマーカーを表示
    new google.maps.Marker({
        position: currentPosition,
        map: map,
        title: 'Your Location'
    });
}


// 地名から位置情報を取得し、マップと現在の位置情報に反映する関数
function geocodeAndShowLocation() {
  // 入力された地名を取得
  var inputAddress = document.getElementById('input-address').value;

  // Geocodingサービスを利用して位置情報を取得
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({ 'address': inputAddress }, function (results, status) {
      if (status === 'OK') {
          // 取得した位置情報の最初の結果を使用
          var location = results[0].geometry.location;
          
          // マップの中心を更新
          map.setCenter(location);

          // マーカーを表示
          new google.maps.Marker({
              position: location,
              map: map,
              title: 'Searched Location'
          });

          // 現在の位置情報を更新
          currentPosition = { lat: location.lat(), lng: location.lng() };
          document.getElementById('latitude').value = currentPosition.lat;
          document.getElementById('longitude').value = currentPosition.lng;
      } else {
          console.error('Geocodingに失敗しました', status);
      }
  });
}

// 検索フォームのsubmitイベントに関数を割り当て
document.querySelector('form').addEventListener('submit', function (event) {
  event.preventDefault(); // デフォルトのsubmit動作を防止
  geocodeAndShowLocation(); // 地名から位置情報を取得して表示
});


