// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCZcMidr4w1kSQ-ATtW3-dYCXlPPrqstYc",
  authDomain: "projspena-463708-ea8b8.firebaseapp.com",
  projectId: "projspena-463708-ea8b8",
  storageBucket: "projspena-463708-ea8b8.firebasestorage.app",
  messagingSenderId: "287678895596",
  appId: "1:287678895596:web:a99a393de3f1a739b51cc9",
  measurementId: "G-N2DRPX2Q8S"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);