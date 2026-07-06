import { Box, Button, Typography } from "@mui/material";

export default function Sidebar() {
    return (

        <Box
            sx={{
                width: 300,
                borderRight: "1px solid #ddd",
                padding: 2
            }}
        >

            <Typography variant="h6">

                Documents

            </Typography>

            <Button
                fullWidth
                variant="contained"
                sx={{ mt: 2 }}
            >

                Upload PDF

            </Button>

        </Box>
    );
}