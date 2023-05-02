// api.ts
import axios from 'axios';

export const getPlayerMeta = async (baseUrl: string, playerName: string) => {
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

export const getPlayerData = async (baseUrl: string, playerName: string, year: number) => {
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

export const getQBOverallData= async (baseUrl: string, topX: string, field: string) => {
    try {
        const response = await axios.get(`${baseUrl}/overall_rankings_top`, {
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


export const getQBWeekData= async (baseUrl: string, topX: string) => {
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


export const getQBOverallDataPlayer= async (baseUrl: string, playerName: string) => {
    try {
        console.log("QUERY PLAYER NAME: ", playerName)
        const response = await axios.get(`${baseUrl}/overall_rankings_player`, {
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