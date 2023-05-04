// api.ts
import axios from 'axios';

// export const base_url = "http://localhost:5000";
export const base_url = '/'
export const getPlayerMeta = 
async (playerName: string) => {
    const baseUrl = import.meta.env.REACT_APP_API_URL;

    try {
        const response = await axios.get(`${baseUrl}/player_meta`, {
            params: {
                player_name: playerName,
            },
           
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching player meta data: ${error}`);
        return null;
    }
};

export const getPlayerData = async (playerName: string, year: number) => {
    const baseUrl = import.meta.env.REACT_APP_API_URL;
    try {
        const response = await axios.get(`${baseUrl}/player_data`, {
            params: {
                player_name: playerName,
                year: year,
            },
           
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching player data: ${error}`);
        return null;
    }
};

export const getQBOverallData= async (topX: string, field: string) => {
    const baseUrl = import.meta.env.REACT_APP_API_URL;
    try {
        const response = await axios.get(`${baseUrl}/overall_rankings_top`, {
            withCredentials: true,
            params: {
                top_x: topX,
                field: field,
            },
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching QB Overall Data: ${error}`);
        return null;
    }
};


export const getQBWeekData= async (topX: string) => {
    const baseUrl = import.meta.env.REACT_APP_API_URL;
    try {
        const response = await axios.get(`${baseUrl}/weekly_rankings`, {
            params: {
                top_x: topX,
            },

        });
        
        return response.data;
    } catch (error) {
        console.error(`Error fetching QB Week Data: ${error}`);
        return null;
    }
};


export const getQBOverallDataPlayer= async ( playerName: string) => {
    const baseUrl = import.meta.env.REACT_APP_API_URL;
    try {
        console.log("QUERY PLAYER NAME: ", playerName)
        const response = await axios.get(`${baseUrl}/overall_rankings_player`, {
            // withCredentials: true,
            params: {
                player_name: playerName,
            },
           
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching QB Overall Data: ${error}`);
        return null;
    }
};