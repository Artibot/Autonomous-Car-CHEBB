/*
	#loadgraph.cs#
	Author -- Eivind Haldorsen
			|| Artibot

*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Threading;
using MLAgents;
using System.Linq;
using Google.Protobuf;
using MLAgents.CommunicatorObjects;
using TensorFlow;


/*
	--------------------------------------------------------
	This class will perform predictions with
	selected tensorflow graph generated in python.
	
	It has different configuration options related to
	the predictions, which includes settings width/height inputs to network,
	threading options, output manipulations such as steering and throttle 
	enhancers, as well as how often to perform predictions.
	--------------------------------------------------------
*/

public class loadGraph : MonoBehaviour
{
	//Public game assets/objects
    public TextAsset graphModel;                            // The trained TensorFlow graph
    public GameObject car;
    public Camera inCam;
    public GameObject stopPanel;
    Car cr;
	//end
	
	//Public configuration variables
    private static int img_width = 150;                      // Image width
    private static int img_height = 150;                     // Image height
    public int frameEvaluationDelay = 5;                     //Frames delay between each evaluation of scenario
	public bool useRealOutput = false;
    private bool threadInit = false;
    public bool useThrot = false;
    public float customSpeed = 1.0f;
    public float steerEnhancer = 1.0f;
    public float throttleEnhancer = 1.0f;
    //end
	
	//Public/private calculation variables	
    private bool isReady = false;
    float[,,,] inputImg =
        new float[1, img_width, img_height, 3];
    public bool useThread = false;
    private float steerVal = 0.0f;
    private float throttleVal = 0.0f;
    private int timm = 0;
	//end
	
	//Tensorflow graph/session declaration
    TFGraph graph = new TFGraph();
    TFSession session;
    TFSession.Runner runner;
	//end

	//This "update" function is called once per frame
    void Update()
    {
		//Usign timer to determine how often we want to predict
        timm += 1;
        if (timm >= frameEvaluationDelay)
        {
           fetchInputImage();
            if (useThread) //Using threading or not
            {
                Thread thr = new Thread(Evaluate);
                thr.Start();
            }
            else
            {
                Evaluate();
            }
           timm = 0;
        }
        isReady = stopPanel.activeSelf;
    }


    void Start()
    {
        cr.SetSpeed(0);
    }
	
    void Awake()
    {
		//Initalize graph/session
        print("Initalizing graph...");
        graph = new TFGraph();
        graph.Import(graphModel.bytes);
        session = new TFSession(graph);
        print("Graph loaded.");
        print("Initalizing thread...");
        cr = car.GetComponent("Car") as Car;
    }

	/*	
		fetchInputImage function retrieves image input from the game scene
		and stores the RGB values in a corresponding array that can be further used to predict.
	*/
    void fetchInputImage()
    {
        Texture2D input = new Texture2D(inCam.targetTexture.width, inCam.targetTexture.height);
        RenderTexture.active = inCam.targetTexture;
        input.ReadPixels(new Rect(0, 0, inCam.targetTexture.width, inCam.targetTexture.height), 0, 0);
        input.Apply();

        // Get raw pixel values from texture, format for inputImg array
        for (int i = 0; i < img_width; i++)
        {
            for (int j = 0; j < img_height; j++)
            {
                inputImg[0, img_width - i - 1, j, 0] = input.GetPixel(j, i).r;
                inputImg[0, img_width - i - 1, j, 1] = input.GetPixel(j, i).g;
                inputImg[0, img_width - i - 1, j, 2] = input.GetPixel(j, i).b;
            }
        }
    }

    /*
		This is the evaluation function, which uses the image input array
		and performs a prediction using the selected neural network model.
	*/
    void Evaluate()
    {
		//Fetch inputs and send them to the model
        var runner = session.GetRunner();
        runner.AddInput(graph["input_1"][0], inputImg);
        runner.Fetch(graph["Output0"][0]);
		
		//Get outputs and store them in a tensor (array)
        float[,] recurrent_tensor = runner.Run()[0].GetValue() as float[,];
		
        steerVal = recurrent_tensor[0, 0];
        if (useThrot) {
            throttleVal = recurrent_tensor[0, 1];
        } else
        {
            throttleVal = customSpeed;
        }
        if (isReady)
        {
            if (throttleVal < 3)
            {
                throttleVal = 3;
            }
			
			//Access the car's steering and throttle/velocity
            cr.RequestSteering(steerEnhancer * steerVal);
            cr.SetSpeed(throttleVal * throttleEnhancer);
        } else
        {
            cr.SetSpeed(0);
        }
        if (!threadInit)
        {
            print("Thread loaded.");
            threadInit = true;
        }
    }
}