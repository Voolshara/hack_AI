<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
import { loadYmap } from "vue-yandex-maps";
export default {
  name: "Map",
  async mounted() {
    const map_settings = {
      apiKey: "49ba2530-8257-44cb-b1cb-a19fb39e046c",
      lang: "ru_RU",
      coordorder: "latlong",
      version: "2.1",
    };
    await loadYmap({ map_settings, debug: true });
    ymaps.ready(function () {
      var customItemContentLayout = ymaps.templateLayoutFactory.createClass(
        // Флаг "raw" означает, что данные вставляют "как есть" без экранирования html.
        "<h2 class=ballon_header>{{ properties.balloonContentHeader|raw }}</h2>" +
          "<div class=ballon_body>{{ properties.balloonContentBody|raw }}</div>" +
          "<div class=ballon_footer>{{ properties.balloonContentFooter|raw }}</div>"
      );
      var myMap = new ymaps.Map(
          "map",
          {
            center: [56.13521435, 47.25730915399754],
            zoom: 13,
          },
          {
            searchControlProvider: "yandex#search",
          }
        ),
        clusterer = new ymaps.Clusterer({
          clusterDisableClickZoom: true,
          clusterOpenBalloonOnClick: true,
          clusterBalloonContentLayout: "cluster#balloonCarousel",
          clusterBalloonItemContentLayout: customItemContentLayout,
          // Макет метки кластера pieChart.
          clusterIconLayout: "default#pieChart",
          // Радиус диаграммы в пикселях.
          clusterIconPieChartRadius: 25,
          // Радиус центральной части макета.
          clusterIconPieChartCoreRadius: 10,
          // Ширина линий-разделителей секторов и внешней обводки диаграммы.
          clusterIconPieChartStrokeWidth: 3,
          // Определяет наличие поля balloon.
        }),
        r = fetch("http://127.0.0.1:5000/get_placemark", {
          method: "POST", // *GET, POST, PUT, DELETE, etc.
          mode: "cors", // no-cors, *cors, same-origin
          cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
          credentials: "same-origin", // include, *same-origin, omit
          headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          redirect: "follow", // manual, *follow, error
          referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
          body: {}, // body data type must match "Content-Type" header
        })
          .then((response) => response.json())
          .then((data) => {
            var geoObjects = [];
            for (var i = 0, len = data["placemarks"].length; i < len; i++) {
              geoObjects[i] = new ymaps.Placemark(
                data["placemarks"][i],
                {
                  balloonContentHeader: data["baloon"][i][1],
                  balloonContentBody: data["baloon"][i][2],
                  balloonContentFooter: data["baloon"][i][0],
                },
                {
                  iconColor: data["colors"][i],
                }
              );
            }

            clusterer.add(geoObjects);
            clusterer.events.add("balloonopen", function (e) {
              // Получим объект, на котором открылся балун.
              var clusterPlacemark = e.get("cluster");
              console.log(clusterPlacemark.geometry._coordinates);
            });
            // clusterer.balloon.open(clusterer.getClusters()[0]);
            myMap.geoObjects.add(clusterer);
            objects
              .searchInside(myMap)
              // И затем добавим найденные объекты на карту.
              .addToMap(myMap);

            circle = new ymaps.Circle(
              [[56.13521435, 47.25730915399754], 100000000000],
              null,
              {
                draggable: true,
              }
            );
            myMap.geoObjects.add(circle);
            circle.events.add("drag", function () {
              // Объекты, попадающие в круг, будут становиться красными.
              var objectsInsideCircle = objects.searchInside(circle);
              objectsInsideCircle.setOptions("preset", "islands#redIcon");
              // Оставшиеся объекты - синими.
              objects
                .remove(objectsInsideCircle)
                .setOptions("preset", "islands#blueIcon");
            });

            myMap.events.add("boundschange", function () {
              // После каждого сдвига карты будем смотреть, какие объекты попадают в видимую область.
              var visibleObjects = objects.searchInside(myMap).addToMap(myMap);
              // Оставшиеся объекты будем удалять с карты.
              objects.remove(visibleObjects).removeFromMap(myMap);
            });
          })
          .catch((error) => {
            console.log("Error:", error);
          });
    });
  },
};
</script>

<style scoped>
#map {
  margin: 0;
  padding: 0;
  width: 80vw;
  height: 80vh;
}
</style>
