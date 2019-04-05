/*
	#Car.cs#
	Author -- Eivind Haldorsen
			|| Artibot
*/
using UnityEngine;
using System.Collections;
using MLAgents;

/*
	This class will handle the cars movement and physics, and
	apply corresponding forces to the wheels using torque and
	steering requests, as well as getters and setters for
	communication with environment.
*/
public class Car : MonoBehaviour {  //MonoBehavior

	//Public game assets / objects
	public WheelCollider[] wheelColliders;
	public Transform[] wheelMeshes;
    public PIDController pidc;
    public Transform centrOfMass;
    public GameObject gruo;
	Rigidbody rb;
	//end
	
	//Public configuration variables
	public float maxTorque = 50f;
	public float maxSpeed = 10f;
    public float vehicleFriction = 0.0005f;
    public bool useJoystick = false;
	//end
	
	//Public/private calculation variables
	public float requestTorque = 0f;
	public float requestBrake = 0f;
	public float requestSteering = 0f;
	public Vector3 acceleration = Vector3.zero;
	public Vector3 prevVel = Vector3.zero;
	public Vector3 startPos;
	public Quaternion startRot;
    public float avgspeed = 0.0f;
    public int speedCounter = 0;
    private float myCurSpeed = 0.0f;
    private float spdd = 0.0f;
    public float length = 1.7f;
	public float lastSteer = 0.0f;
	public float lastAccel = 0.0f;
	public float humanSteeringMax = 15.0f;
	public string activity = "keep_lane";
	//end


    // Use this for initialization
    void Awake () 
	{
		rb = GetComponent<Rigidbody>();
		if(rb && centrOfMass)
		{
			rb.centerOfMass = centrOfMass.localPosition;
		}
		requestTorque = 0f;
		requestSteering = 0f;
        SavePosRot();

    }

	//Save positional rotation for respawns
	public void SavePosRot()
	{
        startPos = transform.position;
        startRot = transform.rotation;
    }

	//Save positional placements for respawns
	public void RestorePosRot()
	{
        Set(startPos, startRot);
        RandomFaces rf = gruo.GetComponent<RandomFaces>();
        rf.updateTexture();
        rb.velocity = Vector3.zero;
        rb.angularVelocity = Vector3.zero;
    }

	//Request/set throttle
	public void RequestThrottle(float val)
	{
        if (!useJoystick) {
            requestTorque = val;
        } 
	}

	//Request/set steering
    public void RequestSteering(float val)
    {
            requestSteering = val;
    }

	/*
		Set position function for manipulating and
		changing the car's position and rotation.
		This is called when the car reaches end of road.	
	*/
    public void Set(Vector3 pos, Quaternion rot)
	{
		rb.position = pos;
        rb.rotation = rot;
		StartCoroutine(KeepSetting(pos, rot, 10));
	}

	IEnumerator KeepSetting(Vector3 pos, Quaternion rot, int numIter)
    {
        while (numIter > 0)
        {
            rb.position = pos;
            rb.rotation = rot;
            transform.position = pos;
            transform.rotation = rot;
			numIter--;
			yield return new WaitForFixedUpdate();
        }
    }

	/*
		Get functions for setting car physics and attributes
	*/
	public float GetSteering()
	{
		return requestSteering;
    }

    public float getMaxSteerAngle()
    {
        return humanSteeringMax;
    }

    public float GetThrottle()
	{
		return requestTorque;
	}

	public float GetFootBrake()
	{
		return requestBrake;
	}

	public float GetHandBrake()
	{
		return 0.0f;
	}

	public Vector3 GetVelocity()
	{
		return rb.velocity;
	}

    public float GetMagnitude()
    {
        return rb.velocity.magnitude;
    }
	
	/*
		Update function to handle joystick and car velocites/steering angles	
	*/
	
	void Update ()
    {
        if (Vector3.Dot(this.transform.forward, Vector3.Normalize(rb.velocity)) < 0)
        {
            rb.velocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
        }
        if (!useJoystick)
        {
            if (pidc.getPrevErr() >= 6 || pidc.getPrevErr() <= -6)
            {
                pidc.endOfPathCB.Invoke();
            }
        }
        else
        {
            float joyIn = Input.GetAxis("HorizontalJoyX");
            float hstm = Mathf.Pow(joyIn, 2);
            requestSteering = Mathf.Sign(joyIn) * humanSteeringMax * hstm;
        }
	}
    
	//Check if using joystick to generate dataset
    public bool getUseJoystick()
    {
        return useJoystick;
    }
	
	//Set speed used by loadGraph.cs which is received from neural network model
    public void SetSpeed(float spd)
    {
        myCurSpeed = spd;
    }

	/*
		Function to update car wheel torque and angle each
		frame interval to generate car movement.	
	*/
    void FixedUpdate()
    {
        lastSteer = requestSteering;
		lastAccel = requestTorque;

        float brake = requestBrake;
        float throttle = requestTorque * maxTorque;


        rb.drag = vehicleFriction - (vehicleFriction * requestTorque);
        if (useJoystick)
        {
            float joyInBrake = Input.GetAxis("BrakeJoy");
            requestBrake = joyInBrake;
            requestTorque = 0;
            if (requestBrake == 0)
            {
                Quaternion targetRot = Quaternion.LookRotation(rb.transform.position, Vector3.up);
                float joyInThrot = Input.GetAxis("ThrottleJoy");
                rb.velocity = transform.forward * (joyInThrot* maxSpeed);
            }
        } else
        {
            requestTorque = 1.0f;
        }
        float steerAngle = requestSteering;


		//Set wheel angles
		wheelColliders[2].steerAngle = steerAngle;
		wheelColliders[3].steerAngle = steerAngle;
		foreach(WheelCollider wc in wheelColliders)
		{
			if(rb.velocity.magnitude < maxSpeed)
			{
				wc.motorTorque = throttle;
			}
			else
			{
				wc.motorTorque = 0.0f;
			}

            wc.brakeTorque = 75f * brake;
		}
		acceleration = rb.velocity - prevVel;
	}
}