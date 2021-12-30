import React, { useState, useEffect } from "react";
import {useDropzone} from 'react-dropzone'
import { Typography, Grid, makeStyles, Button, Link} from "@material-ui/core";
import Helmet from 'react-helmet';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from 'axios'


const useStyles = makeStyles((theme) => ({
  buttonWrapper:{
    marginTop: theme.spacing(4),
    textAlign: "center",
    position: "relative",
  },
  button:{
    minHeight: "50px",
    minWidth: "100px",
  },
  dropContainer:{
    textAlign: "center",
    minHeight: "400px",
    marginTop: theme.spacing(4),
    backgroundColor: "white",
    opacity: "0.1",
    borderRadius: "25px",
    cursor: "pointer",
  },
  title:{
    textAlign: "center",
    marginTop: theme.spacing(4),
  },
  hint:{
    paddingTop: theme.spacing(16)
  },
  svgIcon:{
    paddingTop: theme.spacing(2),
    transform: "scale(4)"
  },
  winnerWrapper:{
    textAlign: "center"
  },
  customTypo:{
    color: "black",
    '&:hover': {
      color: "#32C1CD"
    }
  },
  title2:{
    textAlign: "center",
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(2),
  },
  accepted:{
    paddingTop: theme.spacing(22),
  },
  buttonSpinner: {
    position: "absolute",
    top: "50%",
    left: "50%",
    marginTop: "-12px",
    marginLeft: "-12PX",
  }
}));


function App() {
  const classes = useStyles();
  const {acceptedFiles, getRootProps, getInputProps} = useDropzone({
    accept: 'image/*',
    maxFiles: '1',
    maxSize: 10000000,
  });
  const [winners, setWinners] = useState([]);
  const [showResult, setShowResult] = useState(false);
  const [showFile, setShowFile] = useState(false);
  const [spinning, setSpinning] = useState(false);

  const acceptedFileItem = acceptedFiles.map(file => (
    <Typography variant="h4" key={file.name}>
      {file.path}
    </Typography>
  ));

  const submit = () => {
    setSpinning(true);
    //spinning starts

    const fd = new FormData();
    fd.append('file', acceptedFiles[0]);
    axios.post('http://localhost:8000/upload', fd, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'accept': 'application/json'
      }
    })
      .then(res =>{
        console.log(res.data)
        setWinners(res.data);
        setShowResult(true);
        //spinning ends
      })
  }

  const winnerItem = winners.map(winner => (
    <div key={winner[4]} >
      <Link href={winner[1]} underline="none">
        <Typography variant="h4" className={classes.customTypo}>
          {winner[0]}
        </Typography>
        <img src={winner[2]} width="500px"/>
      </Link>
    </div>
  ));

  useEffect(() => {
    if(acceptedFiles.length !== 0){
      setShowFile(true)
    }
  }, [acceptedFiles])

  return (
    <Grid 
     container
     justifyContent="center"
    >
      <Grid item xs={12} sm={12} md={12} lg={12} className={classes.title}>
        <Typography display="inline" variant="h1" color="secondary">
          {"VS Code Theme "}
        </Typography>
        <Typography display="inline" variant="h1" color="primary">
          {"Finder"}
        </Typography>
      </Grid>
      <Grid item xs={12} sm={10} md={8} lg={4} >
        <div {...getRootProps({className: 'dropzone'})} className={classes.dropContainer} style={{display: showResult? 'none' : 'block'}}>
          <input {...getInputProps()}/>
          <Typography className={classes.hint} variant="h5" style={{display: showFile? 'none' : 'block'}}> 
            Click or drag and drop an image here
          </Typography>
          <CloudUploadIcon className={classes.svgIcon} style={{display: showFile? 'none' : 'inline-block'}}/>
          <div className={classes.accepted}>
          {acceptedFileItem}
          </div>
        </div>
      </Grid>
      <Grid item xs={12} sm={12} className={classes.buttonWrapper} style={{display: showResult? 'none' : 'block'}}>
        <Button
         variant="contained"
         color = "primary"
         className={classes.button}
         onClick={submit}
         disabled={showFile === false || spinning === true}
        >
          <Typography variant="h6">
            Search
          </Typography>
        </Button>
        {spinning === true && <CircularProgress size={24} className={classes.buttonSpinner}/>}
      </Grid>
      <Grid item xs={12} sm={12} className={classes.buttonWrapper} style={{display: showResult? 'block' : 'none'}}>
        <Button
         variant="contained"
         color = "primary"
         className={classes.button}
         onClick={()=> window.location.reload()}
        >
          <Typography variant="h6">
            Go again
          </Typography>
        </Button>
      </Grid>
      <Helmet 
       bodyAttributes={{
        style: 'background-image: linear-gradient(to bottom right, rgb(84, 65, 121) 0%, rgb(97, 102, 179) 100%); min-height: 100%;',
       }}
       htmlAttributes={{
        style: 'min-height: 100%;'
       }}
      />
      <Grid item xs={12} sm={12} className={classes.title2} style={{display: showResult? 'block' : 'none'}}>
        <Typography variant="h2" color="secondary">
          Top results
        </Typography>
      </Grid>
      <Grid item>
        <div className={classes.winnerWrapper}>
          {winnerItem}
        </div>
      </Grid>
    </Grid>
  );
}

export default App;
