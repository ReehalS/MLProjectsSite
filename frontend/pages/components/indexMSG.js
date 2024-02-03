import axios from "axios";
import {useState, useEffect} from "react";

const IndexMSG = () => {
    const [msg, setMsg] = useState(null);
    useEffect(() => {
        const fetchMessage = async () => {
            try{
                const res= await axios.get("http://localhost:8080");
                console.log("RES", res);
                setMsg(res.data);
            }
            catch(err){
                console.log("ERR", err);
            }
        }
    fetchMessage();
}, []);

    return(
        <div>
            <h1>Message from backend</h1>
            {msg? (
                <div>
                    <h2>{msg.message}</h2>
                    {msg.people.map((person,index) => (
                        <h3 key={index}>{person}</h3>
                        ))}
                </div>
                ) : (
                    <h2>Loading...</h2>
                )}
        </div>
    )
}

export default IndexMSG;