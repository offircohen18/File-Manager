import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyA9rSGGguLmWUsGEn8DpXZ2ZvK0xeGtdak",
  authDomain: "file-manager-app-24604.firebaseapp.com",
  projectId: "file-manager-app-24604",
  storageBucket: "file-manager-app-24604.appspot.com",
  messagingSenderId: "471029944740",
  appId: "1:471029944740:web:1e89dcce361afbd78ab131",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, signInWithPopup, signOut };
