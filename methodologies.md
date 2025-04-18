
- How to compute energy for SCI? (Direct, CPU, Dashboard)
- How to get I for SCI? (Hardcode, WattTime, EM)
- How to get embodied for SCI? (Research, Model)
- How to get another SCI? Research/Analog/Experimemt


You now need the following observations parameters in our input array:

- `memory-utilisation`
- `memory-coefficient`
- `carbon-intensity`

```yaml
inputs:
  - timestamp: 2023-08-06T00:00
    duration: 3600
    memory-utilization: 8.8
    memory-coefficient: 0.00039
    carbon-intensity: 163
```

Now you can run the IMP using:

```yaml
if-run -m imp.yml
```

So, you got to your carbon value again, this time you had to make two steps from your observation to your impact:

```yaml
**➜ if-run -m imp.yml**

# start
name: memory-to-carbon
description: minimal demo
tags: null
initialize:
  plugins:
    memory-to-energy-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - memory-utilization
          - memory-coefficient
        output-parameter: energy
    energy-to-carbon-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - energy
          - carbon-intensity
        output-parameter: carbon
execution:
  command: >-
    /Users/russell/.nvm/versions/node/v22.13.1/bin/node /usr/local/bin/if-run -m
    imp.yml
  environment:
    ...
  status: success
tree:
  children:
    component-1:
      defaults: null
      pipeline:
        compute:
          - memory-to-energy-component-1
          - energy-to-carbon-component-1
      inputs:
        - timestamp: 2023-08-06T00:00
          duration: 3600
          memory-utilization: 8.8
          memory-coefficient: 0.00039
          carbon-intensity: 163
      **outputs:**
        - timestamp: 2023-08-06T00:00
          duration: 3600
          memory-utilization: 8.8
          memory-coefficient: 0.00039
          carbon-intensity: 163
          energy: 0.003432
          **carbon: 0.559416**

# end
````

<aside>
<img src="/icons/computer-chip_blue.svg" alt="/icons/computer-chip_blue.svg" width="40px" />

## Get Hands-on

*You can try building and running this IMP for yourself by breaking out to an interactive environment:*

[green software r&d | Killercoda](https://killercoda.com/jcook/course/if-training-course/exercise-3)

</aside>

## Tutorial

## **Creating your manifest**

In this example, rather than having `energy` given to you, you have to apply another model to get `energy` from memory utilisation. The output from one model (memory utilisation to energy) is the input to the next (energy to carbon).

Let’s build this in a manifest file.

Start with the boilerplate again (`boilerplate.yml` ), which you can open in your editor.

## **Add plugins**

Create two instances of the `Multiply` plugin with different names.  The first can be `memory-to-energy-component-1` and it will multiply `memory-utilization` by `memory-coefficient` to yield `energy` . The second can be called `energy-to-carbon-component-1` and it will multiply `energy` by `carbon-intensity` to yield `carbon` . Add these to the `initialize:plugins` block.

If you need some help, take a peek at `manifest-example.yml` .

## **Invoke the plugins in your component**

Now you have two plugin instances available, you can add them to the `pipeline` for your component. Again, for help, see `manifest-example.yml`

Save your manifest as `manifest.yml`

## **Run your manifest**

Now use `if-run -m manifest.yml -o outputs.yml` to run your manifest.

## **View the outputs**

You just created `outputs.yml` .

Open that file in your editor.

You will see that two new values have been added to your `outputs` : `energy` and `carbon` .

Notice that `energy` was not available in the original manifest. It was created when the `memory-to-energy-component-1` plugin ran. Then it was used as the input to `energy-to-carbon-component-1` .

If you remove `memory-to-energy-component-1` from your pipeline and run the manifest again, it will fail. This is because `energy` is a necessary input to `energy-to-carbon-component-1` . By omitting the first plugin, you are starving the second plugin of its input data.

This is an important concept in Impact Framework because it means the order of plugin execution in each component is very important.

## **Test your learning**

1. Try adding another plugin that depends on a `carbon` value being available. Notice that this plugin will run successfully if it is placed in the last position in the pipeline, but it will fail if it is placed anywhere else.

# Key Takeaways

---

<aside>
<img src="/icons/rocket_green.svg" alt="/icons/rocket_green.svg" width="40px" />

- You learned how to handle IMPs with multiple plugins
- You saw how outputs from one plugin can feed into subsequent plugins as inputs
- You learned how to construct a simple multi-step pipeline in an IMP file using the standard library of plugins

</aside>

---

#######################################################################################


Asims Notes:

- Completing the Basic Carbon score (merge with previous section)
    - Here we are adding another type of observation, cpu utilization
    - Choose methodology (in this case we are using again, research) - present alternatives, explain this isn’t a good method but convenient for teaching. Kepler, Scaphandre, other solutions which directly measure power is good, refer to the beginners guide to energy measurement paper from Akshaya.
    - Once you’ve decided select the plugins and pipeline to implement that methodology.
- Multiple components, servers
    - Now we show people how to add multiple components.
    - But this also means this is the section where we should talk about aggregation.
- Then we move into calculating a SCI score.
    - This again means we have changed the
    - The impact has now changed from carbon → SCI. Which means we need to find another set of models and adjust the pipeline to generate a SCI score.
    - We also need to talk about embodied with the SCIEmbodied model.
- Time
    - Now let’s add time as a component, observation arrays etc…
    - We need to discuss observations, we need to discuss why this is important, etc…

# Multiple Observations

---

In the previous module we worked with just memory utilisation, of course that is just one of many energy consuming elements in an application. There are typically several components that have to be summed together to estimate the total carbon for an application. In this example, you’ll build on the previous manifest. 

Imagine that instead of returning only memory utilisation, your monitor API also returns CPU utilisation. CPU utilisation is a bit more complicated to compute than memory utilisation, because it is not done with a simple coefficient. Instead, you have to use the [Thermal Design Power (TDP)](https://www.intel.com/content/www/us/en/support/articles/000055611/processors.html) of the processor being used and a power curve that relates the CPU utilisation to a multiplier that can be applied to the TDP to estimate the power drawn by the CPU.

<aside>
<img src="/icons/book-closed_gray.svg" alt="/icons/book-closed_gray.svg" width="40px" />

See Kepler, Scaphandre etc..

</aside>

## CPU Utilisation & Power

The reason this is necessary is that **power and utilisation are not linearly related** and the curve does not intercept at zero, meaning that an idling processor can consume 50–70% of the energy of a fully utilised one.

![image.png](attachment:f10ea418-83a8-4040-8015-9a4e8e72e90f:image.png)

Therefore, there are several steps that are needed to incorporate CPU utilisation into our estimate of carbon emissions:

1. Find appropriate power curve
2. Interpolate the power curve at the CPU utilisation value to find the `tdp-factor`
3. Multiply the processor TDP by the `tdp-factor`
4. Multiply **Power** by **Time** to give **Energy**
5. Multiply **Energy** by **Carbon Intensity** to give **Carbon**

[Worth having a visual to represent?]

Finding an appropriate power curve is challenging. Ideally, we would have a specific power curve for every individual processor, but this is challenging to obtain. Often, people fall back to a [generalised power curve from this article](https://medium.com/teads-engineering/building-an-aws-ec2-carbon-emissions-dataset-3f0fd76c98ac). You will use that generalised curve here too, for convenience.

<aside>
<img src="/icons/book-closed_gray.svg" alt="/icons/book-closed_gray.svg" width="40px" />

Read more https://if.greensoftware.foundation/pipelines/teads/

</aside>

Your current manifest includes two plugins, `memory-to-energy-component-1` and `energy-to-carbon-component-1`:

```yaml
name: memory-to-carbon
description: minimal demo
tags: null
initialize:
  plugins:
    memory-to-energy-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - memory-utilization
          - memory-coefficient
        output-parameter: energy
    energy-to-carbon-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - energy
          - carbon-intensity
        output-parameter: carbon
tree:
  children:
    component-1:
      defaults: null
      pipeline:
        compute:
          - memory-to-energy-component-1
          - energy-to-carbon-component-1
      inputs:
        - timestamp: 2023-08-06T00:00
          duration: 3600
          memory-utilization: 8.8
          memory-coefficient: 0.00039
          carbon-intensity: 163
      outputs:
        - timestamp: 2023-08-06T00:00
          duration: 3600
          memory-utilization: 8.8
          memory-coefficient: 0.00039
          carbon-intensity: 163
          energy: 0.003432
          carbon: 0.559416           
```

One important thing to point out is that you are currently yielding `carbon` as the output from the memory utilisation pipeline. However, in the new manifest, `carbon` will not only be the result of memory utilisation; there will be a CPU utilisation component too. 

The summation of the two components should happen before you generate a `carbon` value. There are two options:

- You can sum the energy from memory and the energy from CPU and do a single energy-to-carbon conversion,
- You can independently calculate `carbon` for each component and sum the two `carbon` values together.

In the latter case, the individual carbon values have to be named something other than `carbon` to avoid a naming collision, for example `carbon-cpu` and `carbon-memory`.

In this example, you will sum the energy components and then do a single conversion to `carbon`.

## Power Curve Interpolation

In the `builtins` library, you can find the `Interpolate` plugin. You define the known points on the curve, grabbed from the [article](https://medium.com/teads-engineering/building-an-aws-ec2-carbon-emissions-dataset-3f0fd76c98ac), the interpolation method (use linear point-to-point),  and the point to interpolate at, which is your CPU utilisation value. You’ll name the output `tdp-multiplier` as it is really an intermediate value that needs to be multiplied with the processor TDP to yield the CPU power.

The plugin config looks as follows:

```yaml
interpolate-power-curve:
  method: Interpolation
  path: "builtin"
  config:
    method: linear
    x: [0, 10, 50, 100]
    y: [0.12, 0.32, 0.75, 1.02]
    input-parameter: "cpu-utilization"
    output-parameter: "tdp-multiplier"
```

Next, you can add an instance of `Multiply` to compute the product of `tdp-multiplier` and the processor TDP. To find the right TDP value, you first need to know the instance type you are using, and from there you can look up the processor name and then the TDP. 

Earlier, you determined that you were using an `Azure Standard A2m_v2`. The GSF have a ['Cloud Metadata Azure Instances data set](https://github.com/Green-Software-Foundation/if-data/blob/main/cloud-metdata-azure-instances.csv) that maps instance names to processors and lists their TDPs. For your instance, you are probably using a processor with a TDP of 205 W.

You can use this information to configure your `Multiply` plugin:

```yaml
tdp-multiplier-to-power:
  method: Multiply
  path: builtin
  config:
    input-parameters: ["tdp-multiplier", "tdp"]
    output-parameter: "cpu-power"
```

This yields `power` - since you want `energy` you would usually need to multiply this by time, but since the relevant time period is 1 hour, 1 W = 1Wh, so no additional conversion is needed.

However, you do want the value to be in kWh, so you need to divide by 1000. We’ll name the result `cpu-energy-kwh` :

```yaml
power-to-energy-kwh:
  method: Divide
  path: "builtin"
  config:
    numerator: cpu-power
    denominator: 1000
    output: cpu-energy-kwh
```

Your IMP now looks like:

```yaml
name: memory-to-carbon
description: minimal demo
tags: null
initialize:
  plugins:
    memory-to-energy-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - memory-utilization
          - memory-coefficient
        output-parameter: energy
    energy-to-carbon-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - energy
          - carbon-intensity
        output-parameter: carbon
		interpolate-power-curve:
		  method: Interpolation
		  path: "builtin"
		  config:
		    method: linear
		    x: [0, 10, 50, 100]
		    y: [0.12, 0.32, 0.75, 1.02]
		    input-parameter: "cpu-utilization"
		    output-parameter: "tdp-multiplier"
		tdp-multiplier-to-power:
		  method: Multiply
		  path: builtin
		  config:
		    input-parameters: ["tdp-multiplier", "tdp"]
		    output-parameter: "cpu-power"
		power-to-energy-kwh:
		  method: Divide
		  path: "builtin"
		  config:
		    numerator: cpu-power
		    denominator: 1000
		    output: cpu-energy-kwh		    		    
tree:
  children:
    ...
```

## Energy from Memory & CPU

<aside>
🤔

ASIMS NOTES

A more useful approach here would be to break out the memory, cpu into seperate sub-components. Or at least if we don’t why don’t we? There is a tendency for convenience to mash everything into one component, but if you wanted to see the proportion of one component vs. another then separating them out is useful. We should provide some guidance. 

- If you want to see total groupings across a range of servers for mem, cpu, disk then all of these should be in separate components. NOTE: This is where atomic observations forced into time buckets and the use of groupings works well. Then you could have all the atomic observations that you want, then group them however you want.
- If you don’t think there will be useful information surfaced from seperating them out (e.g. one component is so much larger than another that the others will be superfluous) then perhaps into one shared component of server.
- But basically the question of “do I model a server atomically” or “is a server a grouping of cpu, mem etc.. component nodes” is at least a question people are going to ask in many other forms for other problems. We should have some discussion about it.
</aside>

Now you have a pipeline that generates estimates of `energy` from both the memory utilisation and the CPU utilisation. You can sum them together and convert to carbon.

Remember, you already have a parameter called `energy` that’s output by the `memory-to-energy-component-1` plugin. You’ll want to use `energy` to represent the sum of energy components, so go back and rename the output from `memory-to-energy-component-1` from `energy` to `memory-energy-kwh`.

Next, create an instance of the `Sum` plugin that takes `memory-energy-kwh` and `cpu-energy-kwh` to yield `energy`, as follows:

```yaml
sum-energy-components:
  path: "builtin"
  method: Sum
  config:
    input-parameters:
      - memory-energy-kwh
      - cpu-energy-cpu
    output-parameter: energy
```

Finally, add your new plugins to your pipeline:

```yaml
pipeline:
  compute:
    - memory-to-energy-component-1
    - interpolate-power-curve
    - tdp-multiplier-to-power
    - power-to-energy-kwh
    - sum-energy-components
    - energy-to-carbon-component-1
```

And finally, we need to provide CPU utilisation and TDP data in `inputs`:

```yaml
inputs:
  - timestamp: 2023-08-06T00:00
    duration: 3600
    memory-utilization: 8.8
    cpu-utilization: 80
    tdp: 205
    memory-coefficient: 0.00039
    carbon-intensity: 163
```

Final IMP:

```yaml
name: memory-to-carbon
description: minimal demo
tags: null
initialize:
  plugins:
    memory-to-energy-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - memory-utilization
          - memory-coefficient
        output-parameter: energy
    energy-to-carbon-component-1:
      path: builtin
      method: Multiply
      config:
        input-parameters:
          - energy
          - carbon-intensity
        output-parameter: carbon
		interpolate-power-curve:
		  method: Interpolation
		  path: "builtin"
		  config:
		    method: linear
		    x: [0, 10, 50, 100]
		    y: [0.12, 0.32, 0.75, 1.02]
		    input-parameter: "cpu-utilization"
		    output-parameter: "tdp-multiplier"
		tdp-multiplier-to-power:
		  method: Multiply
		  path: builtin
		  config:
		    input-parameters: ["tdp-multiplier", "tdp"]
		    output-parameter: "cpu-power"
		power-to-energy-kwh:
		  method: Divide
		  path: "builtin"
		  config:
		    numerator: cpu-power
		    denominator: 1000
		    output: cpu-energy-kwh
		sum-energy-components:
		  path: "builtin"
		  method: Sum
		  config:
		    input-parameters:
		      - memory-energy-kwh
		      - cpu-energy-cpu
		    output-parameter: energy		    		    		    
tree:
  children:
    component-1:
      defaults: null
      pipeline:
			  compute:
			    - memory-to-energy-component-1
			    - interpolate-power-curve
			    - tdp-multiplier-to-power
			    - power-to-energy-kwh
			    - sum-energy-components
			    - energy-to-carbon-component-1
      inputs:
			  - timestamp: 2023-08-06T00:00
			    duration: 3600
			    memory-utilization: 8.8
			    cpu-utilization: 80
			    tdp: 205
			    memory-coefficient: 0.00039
			    carbon-intensity: 163
```

Now you can run the IMP using:

```yaml
if-run -m imp.yml
```

<aside>
<img src="/icons/computer-chip_blue.svg" alt="/icons/computer-chip_blue.svg" width="40px" />

## Get Hands-on

*You can try building and running this IMP for yourself by breaking out to an interactive environment:*

[green software r&d | Killercoda](https://killercoda.com/jcook/course/if-training-course/exercise-4)

</aside>

# Tutorial

In this exercise we will build a manifest with multiple plugins. The aim is to observe how the outputs of one plugin become inputs to the next.

On the right hand panel you have terminal access to an environment with Impact Framework already installed.

You also have two files:

`boilerplate.yml` : this contains the basic skeleton of a manifest file, ready for you to complete. `manifest-example.yml` : this is a completed example that you can refer to when you need to.

This is all you need to complete this exercise!

## **Creating your manifest**

In this example, rather than having `energy` given to you, you have to apply another model to get `energy` from memory utilisation. The output from one model (memory utilisation to energy) is the input to the next (energy to carbon).

Let’s build this in a manifest file.

Start with the boilerplate again (`boilerplate.yml` ), which you can open in your editor.

## **Add plugins**

Create two instances of the `Multiply` plugin with different names.  The first can be `memory-to-energy-component-1` and it will multiply `memory-utilization` by `memory-coefficient` to yield `energy` . The second can be called `energy-to-carbon-component-1` and it will multiply `energy` by `carbon-intensity` to yield `carbon` . Add these to the `initialize:plugins` block.

If you need some help, take a peek at `manifest-example.yml` .

## **Invoke the plugins in your component**

Now you have two plugin instances available, you can add them to the `pipeline` for your component. Again, for help, see `manifest-example.yml`

Save your manifest as `manifest.yml`

## **Run your manifest**

Now use `if-run -m manifest.yml -o outputs.yml` to run your manifest.

## **View the outputs**

You just created `outputs.yml` .

Open that file in your editor.

You will see that two new values have been added to your `outputs` : `energy` and `carbon` .

Notice that `energy` was not available in the original manifest. It was created when the `memory-to-energy-component-1` plugin ran. Then it was used as the input to `energy-to-carbon-component-1` .

If you remove `memory-to-energy-component-1` from your pipeline and run the manifest again, it will fail. This is because `energy` is a necessary input to `energy-to-carbon-component-1` . By omitting the first plugin, you are starving the second plugin of its input data.

This is an important concept in Impact Framework because it means the order of plugin execution in each component is very important.

## **Test your learning**

1. Try adding another plugin that depends on a `carbon` value being available. Notice that this plugin will run successfully if it is placed in the last position in the pipeline, but it will fail if it is placed anywhere else.