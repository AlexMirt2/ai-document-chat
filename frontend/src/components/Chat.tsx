import { Box, Typography } from "@mui/material";

export default function Chat() {

    return (

        <Box
            sx={{
                flex: 1,
                padding: 4
            }}
        >

            <Typography variant="h4">

                Welcome 👋

            </Typography>

            <Typography sx={{ mt: 2 }}>

                Upload a document to start chatting.

            </Typography>

        </Box>
    );

}