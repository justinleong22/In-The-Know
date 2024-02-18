import React, { useMemo, useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, SafeAreaView, Button, TextInput, ImageBackground, Image} from 'react-native';
import MapView, { Heatmap, Marker, PROVIDER_GOOGLE, Polygon } from 'react-native-maps';
//import { locations } from './data/data';
import * as Location from 'expo-location';
import { Platform } from 'react-native';
import { Audio } from 'expo-av';
import { Linking } from 'react-native';
import { Switch } from 'react-native';
import { TouchableOpacity } from 'react-native';

const schoolImage = require('./assets/school.png')
const profilePic = require('./assets/profilepic.png')
const shieldImage = require('./assets/shield.png')
//const gifImage = re


export default function App() {
  const [lat, setLat] = useState();
  const [long, setLong] = useState();
  const [distanceFrom, setDistanceFrom] = useState();
  const [locations, setLocations] = useState([]);
  
  const [threatExists, setThreatExists] = useState(false);
  const [currentCoordinate, setCurrentCoordinate] = useState({
    latitude: 26.3043,
    longitude: -80.26764,
  });
  const [shooterLocation, setShooterLocation] = useState({
    latitude: 26.3043,
    longitude: -80.26764
  });
  const [recording, setRecording] = React.useState();
  const [recordings, setRecordings] = React.useState([]);
  const [reportText, setReportText] = useState("")
  const [showGif, setShowGif] = useState(false)


  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3; // Earth radius in meters
    const φ1 = (lat1 * Math.PI) / 180;
    const φ2 = (lat2 * Math.PI) / 180;
    const Δφ = ((lat2 - lat1) * Math.PI) / 180;
    const Δλ = ((lon2 - lon1) * Math.PI) / 180;
    const a =
        Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const d = R * c; // Distance in meters
    return d;
};


  const handleCall = () => {
    const phoneNumber = '9544595315'; 
    Linking.openURL(`tel:${phoneNumber}`);
  }; 

    const fetchData = async () => {
      //console.log("fetchData call recieved")
      try{
      //console.log("Sending Get Request")
      const response = await fetch('http://0.0.0.0:8000/api/shooter_location');

      const data = await response.json()
      const [latitude, longitude] = data;
      
      
      //console.log(data)
      //console.log(latitude)
      //console.log(longitude)
      await setLat(latitude);
      await setLong(longitude);
      // await setShooterLocation({
      //   latitude: latitude,
      //   longitude: longitude
      // })

      await setDistanceFrom(calculateDistance(
        currentCoordinate.latitude,
        currentCoordinate.longitude,
        latitude,
        longitude
        ));

      // await setLocations(prevLocations => [
      //   {
      //     latitude,
      //     longitude,
      //     weight: 2
      //   },
      //    ...prevLocations])

      // console.log("all locations", locations)
      
      // const newLocationInstance = {
      //   latitude: latitude,
      //   longitude: longitude,
      //   weight: 2
      // };
      
      //setLocations([...locations, newLocationInstance])
       } catch(error)
      {
        console.log(error)
      }
    }



    useEffect(() => {
      if (lat !== undefined && long !== undefined) {
        // Create new location instance
        const newLocationInstance = {
          latitude: lat,
          longitude: long,
          weight: 2
        };
        //console.log("New instance: ", newLocationInstance)
    
        // Update locations state
        setLocations(prevLocations => [newLocationInstance, ...prevLocations]);
      }
    }, [lat, long]);

    


    const sendUserData = async () => {
      //getUserLocation();
      const response = await fetch(
        `http://0.0.0.0:8000/api/update`,
        {
          method: 'post',
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            //files: recordings.map(recording => recording.file), // Assuming recording.file contains the file data
            files: [],
            latitude: currentCoordinate.latitude,
            longitude: currentCoordinate.longitude,
            res: 300
          })  
        })
    }


    
  async function startRecording() {
    //console.log("Starting recording")
    try {
      const perm = await Audio.requestPermissionsAsync();
      if (perm.status === "granted") {
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true
        });
        const { recording } = await Audio.Recording.createAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
        setRecording(recording);
      }
    } catch (err) {}
  }

  async function stopRecording() {
    //console.log("Stopping Recording")
    setRecording(undefined);

    await recording.stopAndUnloadAsync();
    let allRecordings = [...recordings];
    const { sound, status } = await recording.createNewLoadedSoundAsync();
    allRecordings.push({
      sound: sound,
      duration: getDurationFormatted(status.durationMillis),
      file: recording.getURI(),
    });

    setRecordings(allRecordings);
    //console.log(recordings);
  }
  

  function getDurationFormatted(milliseconds) {
    const minutes = milliseconds / 1000 / 60;
    const seconds = Math.round((minutes - Math.floor(minutes)) * 60);
    return seconds < 10 ? `${Math.floor(minutes)}:0${seconds}` : `${Math.floor(minutes)}:${seconds}`
  }

  function getRecordingLines() {
    //console.log(recordings)
    return recordings.map((recordingLine, index) => {
      return (
        <View key={index} style={styles.row}>
          <Text style={styles.fill}>
            Recording #{index + 1} | {recordingLine.duration}
          </Text>
          <Button onPress={() => recordingLine.sound.replayAsync()} title="Play"></Button>
        </View>
      );
    });
  }

  function clearRecordings() {
    setRecordings([])
  }
  
  const getUserLocation = async () => {
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        console.error('Permission to access location was denied');
        return;
      }
  
      let location = await Location.getCurrentPositionAsync({});
      //console.log('User location:', location.coords);
      setCurrentCoordinate({
        latitude: location.coords.latitude,
        longitude: location.coords.longitude
      })
    } catch (error) {
      console.error('Error getting user location:', error);
    }
  };
  

  const handleMarkerDragEnd = (e) => {
    const { latitude, longitude } = e.nativeEvent.coordinate;
    setMarkerCoordinate({ latitude, longitude });
    //console.log(latitude, longitude)
    setHasSetMarker(true);
  };


  const myFunction = async () => {
    console.log('Function called every 2 seconds');
    startRecording(); // Start recording
    setTimeout(stopRecording, 3000); // Stop recording after 3 seconds
    setTimeout(() => {console.log(recordings)}, 2000);
  };


  //myFunction();  
  // useEffect(() => {
  //   const intervalId = setInterval(myFunction, 2000);
  //   const intervalId2 = setInterval(stopRecordingAfterDelay, 3000);


  //   return () => {
  //     clearInterval(intervalId)
  //     clearInterval(intervalId2);
  // };
    
  // }, []); // Empty dependency array ensures the effect runs only once after the initial render

  useEffect(() => 
  {
    const intervalId = setInterval(fetchData, 500);
    //const intervalId2 = setInterval(sendUserData, 2000);
    console.log("rendering data")


    return () => {
      clearInterval(intervalId)
      //clearInterval(intervalId2)
  };
}, []); // Empty dependency array ensures the effect runs only once after the initial render

  // if(showGif)
  // {
  //   <SafeAreaView>
  //     <Image 
  //     source={}
  //     style = {{}}
  //     />
  //   </SafeAreaView>
  // }


  if(!threatExists)
  {
    return(
   
       <SafeAreaView>
        <View style = {{flexDirection: 'row', justifyContent: 'space-between'}}>
          <Text style = {{
            fontSize: 15,
          fontWeight: 'bold',
          marginTop: 20,
          marginLeft: 30,
          marginBottom: 25,
    }}>Stoneman Douglas High School</Text>

    <Image
      source = {profilePic}
      style = {{
        width: 50, // Adjust width as needed
        height: 50, // Adjust height as needed
        borderRadius: 30, // Adjust border radius for rounded corners
        marginRight: 20
      }}
    />
    </View>

    <View style = {{alignItems: 'center'}}>
    <Image
    source = {schoolImage}
    style = {{
      width: 350, // Adjust width as needed
    height: 350, // Adjust height as needed
    borderRadius: 20, // Adjust border radius for rounded corners
    alignItems: 'center'
    }}
    />

<Text style = {{
            fontSize: 25,
          marginTop: 20,
          marginLeft: 30,
          marginBottom: 5,
          fontFamily: 'Times New Roman'
    }}>Have a Safe Day, Abishek!</Text>

    </View>

   
    <View style = {{flexDirection: 'row'}}>
    <TouchableOpacity
  onPress={() => {
    setThreatExists(true);
    setShowGif(true);
    handleCall();
    startRecording();
  }}
  style={{
    backgroundColor: 'red',
    width: 200, // Adjust width as needed
    height: 290, // Adjust height as needed
    borderRadius: 25, // Make it a circle
    borderWidth: 3,
    margin: 16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowOffset: { width: 2, height: 2 },
    shadowColor: "#333",
    shadowOpacity: 0.3,
    shadowRadius: 4,
    padding: 10
  }}>
    <Text style = {{
      color: 'white',
      fontSize: 16,
      fontWeight: 'bold',
      fontFamily: "Courier New"
    }}>Report Shots to 911</Text>
</TouchableOpacity>

<View>
<TouchableOpacity
  onPress={() => {
    setThreatExists(true);
    handleCall();
    startRecording();
  }}
  style={{
    backgroundColor: 'green',
    width: 125, // Adjust width as needed
    height: 125, // Adjust height as needed
    borderRadius: 25, // Make it a circle
    borderWidth: 2,
    margin: 16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowOffset: { width: 2, height: 2 },
    shadowColor: "#333",
    shadowOpacity: 0.3,
    shadowRadius: 4,
    padding: 5
  }}>
    <Text style = {{
      color: 'white',
      fontSize: 16,
      fontWeight: 'bold',
      fontFamily: "Courier New"
    }}>Emergency Contacts</Text>
</TouchableOpacity>

<TouchableOpacity
  onPress={() => {
    setThreatExists(true);
    handleCall();
    startRecording();
  }}
  style={{
    backgroundColor: 'blue',
    width: 125, // Adjust width as needed
    height: 125, // Adjust height as needed
    borderRadius: 25, // Make it a circle
    borderWidth: 2,
    margin: 16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowOffset: { width: 2, height: 2 },
    shadowColor: "#333",
    shadowOpacity: 0.3,
    shadowRadius: 4,
    padding: 10
  }}>
    <Text style = {{
      color: 'white',
      fontSize: 16,
      fontWeight: 'bold',
      fontFamily: "Courier New"
    }}>Emergency Contacts</Text>
</TouchableOpacity>

</View>

</View>
      </SafeAreaView> 
    )
  }


  if (threatExists) {
    //getUserLocation();
  
    return (
<View style={styles.container}>
<SafeAreaView>  
<Text style = {styles.card}>
  Estimated Distance From Shooter: {distanceFrom.toFixed(0)}</Text>
</SafeAreaView>
<MapView
provider={'google'}
  style={styles.map}
  initialRegion={{
    latitude: currentCoordinate.latitude,
    longitude: currentCoordinate.longitude,
    latitudeDelta: 0.002,
    longitudeDelta: 0.002,
  }}
  
  //onUserLocationChange={(event) => setUserLocation(event.nativeEvent.coordinate)}
>
  
  <Marker
      coordinate={{
          latitude: lat,
          longitude: long,
        }}
        
  />

    <Marker
      coordinate={{
          latitude: 26.30425,
          longitude: -80.26763,
        }}  
        //pinColor='blue'
         image={require('./assets/pointer1.png')}
      />
      


  <Heatmap points={locations}
  radius = {350}/> 
</MapView>

</View>
    )
}

  //const snapP = useMemo(() => ['25%', '50%', '70%'], [])
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
    overflow: 'hidden'
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
  marker: {
    width: 30,
    height: 30,
  },
  card: {
    backgroundColor : "red",
    borderRadius: 16,
    borderWidth: 2,
    padding: 16,
    margin: 16, 
    overflow: 'hidden' 
},
map: {
  flex: 1, // Take up remaining space
},
row: {
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
  marginLeft: 10,
  marginRight: 40
},
fill: {
  flex: 1,
  margin: 15
},
});




