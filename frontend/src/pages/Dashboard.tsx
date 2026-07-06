import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import Chat from "../components/Chat";

import { Box } from "@mui/material";

export default function Dashboard() {
    return (
        <Box sx={{ height: "100vh" }}>

            <Header />

            <Box
                sx={{
                    display: "flex",
                    height: "calc(100vh - 64px)"
                }}
            >

                <Sidebar />

                <Chat />

            </Box>

        </Box>
    );
}