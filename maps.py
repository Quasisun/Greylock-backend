## Maps key: AIzaSyD0xObEyHQF_wQbDeljl_Q7DqQYhg74Cls
import googlemaps as gmaps
from datetime import datetime
import json
import aco

gmapsKey = 'AIzaSyD2HMu7mFghN26WjCRe8pjBwLFrxyn4kJ0'
gmapsClient = gmaps.Client(key = gmapsKey)

def getNaiveDistance(origin, destination):
#    now = datetime.now()
#    directions_result = gmapsClient.directions(origin, destination,
#                                               mode='driving',
#                                               departure_time=now)
#    distInKm = (directions_result[0]['legs'][0]['distance']['value'])/1000.0
#    return (distInKm * 1.60934)
    return (aco.geoDistance(origin, destination))

def getTotalNaive(locations):
    res = 0.0
    for i in range(1, len(locations)):
        res += getNaiveDistance(locations[i-1], locations[i])

    return res

# Returns the first point on the route between two points
def getRouteIntersections(gmapsClient, origin, destination, maxWalk):
    now = datetime.now()
    directions_result = gmapsClient.directions(origin, destination,
                                               mode='driving',
                                               departure_time=now)
    validIntersections = []
    totalDist = 0
    for leg in directions_result[0]['legs']:
        for step in leg['steps']:
            if totalDist < maxWalk:
                validIntersections.append(((step['end_location']['lat'],
                                            step['end_location']['lng']
                                           ), origin))
                totalDist += step['distance']['value']
            else:
                return validIntersections

    return validIntersections

def addressToLatLngTuple(address):
    location = gmapsClient.geocode(address)
    return location[0]['geometry']['location']

# Returns list of intersections in a route to give to FrontEnd
def getFinalResult(gmapsClient, origin, destination):
    now = datetime.now()
    directions_result = gmapsClient.directions(origin, destination,
                                               mode='driving',
                                               departure_time=now)
    validIntersections = []
    for leg in directions_result[0]['legs']:
        for step in leg['steps']:
            validIntersections.append((step['end_location']['lat'],
                                        step['end_location']['lng']))
    return validIntersections

def testGetRouteIntersection():
    routeIntersectionCoord = getRouteIntersections(
        gmapsClient, \
        "101 McLellan Drive, South San Francisco, CA", \
        "5000 N Ballard Rd, Appleton, WI", \
        50
    )

    print(routeIntersectionCoord)

if __name__ == "__main__":
    testGetRouteIntersection()
