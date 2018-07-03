# Select Example

This is a fuller example containing a Flask API, tied to SQLAlchemy and a SQLITE database, with a front end that has a Leaflet.js map with markers that are shown or not shown based on a selected input.  The options for the selected input are dynamically generated.

## The Data

The data consists of one table: `incident`, that documents incidents of TSA confiscations.  That table has the following columns:

 - index: an id primary key column
 - name: the string name of the airport where the confiscation happened
 - latitude: float latitude of the airport
 - longitude: float longitude of the airport
 - item: string category of the item confiscated
 - date: date of the confiscation incident

## Some Explanation of the API

In the API, the SQLAlchemy table is defined with nice column names and types to help with querying (and to remind me what stuff is).

I leaned heavily on the [VSCode SQLITE Extension](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) to help me with this.

The magic is in the `/data` route.

My query is a group-by two different columns: airport name and confiscated item.  I also query a count of the items.  This returns rows that look like this:

| Name | Lat | Long | Item | Count |
|---|---:|---:|:---:|---:|
| LAX | ... | ... | knife | 3 |
| DFW | ... | ... | gun | 2 |

In order to provide JSON in a useful shape to the front end, I loop through these results and build a dict of the shape:

```python
{
  "LAX": {
    "name": "LAX",
    "lat": ...,
    "long": ...,
    "items": {
      "knife": 3,
      "bazooka": 1,
    }
  },
  "DFW": ...
}
```

I use `defaultdict` from the `collections` module of the standard library to clean up my `for` loop a little.  Basically, if the item isn't in `items`, Python assumes that it has zero.  For example, if items looks like this:

```python
"items": {
  "knife": 3
}
```

and then this gets run:

```python
results[name]["items"]["bazooka"] += 1
```

Python looks for the "bazooka" item in the `items` dict, doesn't find it, creates it, and sets it to zero.  Then it adds one to it like we tell it to.

Lastly, instead of just returning the `results` dict (which we could totally do), I return `list(results.values())`, which is the same thing, but it's a list overall instead of a dictionary.  That way, it's a little easier to loop through on the JS end.

## The JS

For the front end, I load the data with D3 from the route we created in our Flask app.  I then loop through each datapoint (each one is an airport):

```javascript
var markers = [];

d3.json('/data', function (data) {

  data.forEach(function (datapoint) {
    marker = L.marker(datapoint.coords,
      {
        items: datapoint.items,
        name: datapoint.name
      }
    );
    markers.push(marker);
    marker.addTo(mymap);
    Object.keys(datapoint.items).forEach(function(item) {
      items.add(item);
    }
  });

  items.forEach(function (item) {
    const option = document.createElement('option');
    option.innerHTML = item;
    selector.appendChild(option);
  })
});
```

For each datapoint, I create a marker, add the relevant data to that marker, add the marker to my global list of markers, add the marker to the map, and add the items for that datapoint to the master list of items.

Because I'm using a `Set`, we're guaranteed to not have any duplicates.

Lastly, I loop through each of our unique items and build the options for the HTML `select` element.  You can see the rest of the javascript code [in main.js](./static/main.js).