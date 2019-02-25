using System.Collections.Generic;
using UnityEngine;
using MLAgents;


public class RollerAgent : Agent
{
    public Transform Target;
    public Transform Obstacle;

    Rigidbody rBody;
    void Start()
    {
        rBody = GetComponent<Rigidbody>();
        Physics.IgnoreCollision(Target.GetComponent<Collider>(), GetComponent<Collider>());
    }


    //reset agent positon on fall off
    public override void AgentReset()
    {
        if (this.transform.position.y < 0) //pos y < 0, fall off platform
        {
            resetPos();
        }
        // Move the target square to a random pos
        Target.position = new Vector3(Random.value * 8 - 4,
                                                  0.5f,
                                                  Random.value * 8 - 4);
    }

    private void resetPos()
    {
        // If the Agent fell, zero its momentum
        this.rBody.angularVelocity = Vector3.zero; //angular velocity set to zero
        this.rBody.velocity = Vector3.zero;
        // Put position of sphere on center of board
        this.transform.position = new Vector3(2, 0.3f, 2);
    }

    //FUNCTION TO READ INPUTS TO BRAIN (IMPORTANT INFORMATION ABOUT TASK)
    public override void CollectObservations()
    {
        // Target and Agent positions    
        AddVectorObs(Obstacle.position);
        AddVectorObs(Target.position);          //pos of box
        AddVectorObs(this.transform.position);  //pos of agent/sphere

        // Agent velocity
        AddVectorObs(rBody.velocity.x);         //agent velocity x
        AddVectorObs(rBody.velocity.z);         //agent velocity z
    }

    public float speed = 50;
    public override void AgentAction(float[] vectorAction, string textAction)
    {
        // Actions, size = 2
        Vector3 controlSignal = Vector3.zero;
        controlSignal.x = vectorAction[0]; //brain control x force
        controlSignal.z = vectorAction[1]; //brain control z force
        rBody.AddForce(controlSignal * speed);

        // Rewards
        float distanceToTarget = Vector3.Distance(this.transform.position,
                                                  Target.position);
        float distanceToObs = Vector3.Distance(this.transform.position,
                                          Obstacle.position);

        // Reached target
        if (distanceToTarget < 1.42f)
        {
            SetReward(1.0f);
            Done();
            //float prwd = (Time.time - startTime) / (4 * maxTime);
            //startTime = Time.time;
        }

        if (distanceToObs < 1.42f)
        {
            resetPos();
            Done();
        }

        // Fell off platform
        if (this.transform.position.y < 0)
        {
            Done();
        }
    }
}