import React, { useState, useEffect, useRef } from 'react';
import { Terminal } from 'lucide-react';

// Main PASTURE Demo Application
const PastureDemo = () => {
  const [activeTab, setActiveTab] = useState('interactive');
  const [terminalOutput, setTerminalOutput] = useState(["Welcome to PASTURE Interactive Terminal!", "Type 'help' to see available commands."]);
  const [terminalInput, setTerminalInput] = useState('');
  const [modelsLoaded, setModelsLoaded] = useState({
    llama3: false,
    mistral: false,
    phi3: false
  });
  const [pipelineSteps, setPipelineSteps] = useState([]);
  const [pipelineRunning, setPipelineRunning] = useState(false);
  const [cacheStats, setCacheStats] = useState({
    hits: 0,
    misses: 0,
    totalEntries: 0,
    totalSize: '0 KB'
  });
  const [errorState, setErrorState] = useState({
    hasError: false,
    model: '',
    attempts: 0
  });
  
  const terminalRef = useRef(null);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    return () => setIsMounted(false);
  }, []);

  // Focus on terminal input when tab changes
  useEffect(() => {
    if (activeTab === 'interactive') {
      const inputElement = document.querySelector('input[type="text"]');
      if (inputElement) {
        setTimeout(() => inputElement.focus(), 100);
      }
    }
  }, [activeTab]);

  // Auto-scroll terminal
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [terminalOutput]);

  // Function to simulate loading a model
  const loadModel = (model) => {
    addToTerminal(`[ModelManager] Loading model: ${model}...`);
    setModelsLoaded(prev => ({ ...prev, [model]: false }));
    
    setTimeout(() => {
      addToTerminal(`[ModelManager] Model ${model} loaded successfully`);
      setModelsLoaded(prev => ({ ...prev, [model]: true }));
    }, 1500);
  };

  // Function to unload a model
  const unloadModel = (model) => {
    if (modelsLoaded[model]) {
      addToTerminal(`[ModelManager] Unloading model: ${model}...`);
      setTimeout(() => {
        addToTerminal(`[ModelManager] Model ${model} unloaded successfully`);
        setModelsLoaded(prev => ({ ...prev, [model]: false }));
      }, 800);
    } else {
      addToTerminal(`[ModelManager] Model ${model} is not currently loaded`);
    }
  };

  // Function to add text to terminal
  const addToTerminal = (text) => {
    setTerminalOutput(prev => [...prev, text]);
  };

  // Function to process terminal input
  const processCommand = (e) => {
    e.preventDefault();
    
    if (!terminalInput.trim()) return;
    
    const command = terminalInput.trim();
    addToTerminal(`> ${command}`);
    
    // Focus back on input
    setTimeout(() => {
      const inputElement = document.querySelector('input[type="text"]');
      if (inputElement) inputElement.focus();
    }, 50);
    
    // Process command
    if (command.startsWith('load ')) {
      const model = command.split(' ')[1];
      if (['llama3', 'mistral', 'phi3'].includes(model)) {
        loadModel(model);
      } else {
        addToTerminal('Error: Unknown model. Available models: llama3, mistral, phi3');
      }
    } else if (command.startsWith('unload ')) {
      const model = command.split(' ')[1];
      if (['llama3', 'mistral', 'phi3'].includes(model)) {
        unloadModel(model);
      } else {
        addToTerminal('Error: Unknown model. Available models: llama3, mistral, phi3');
      }
    } else if (command === 'help') {
      addToTerminal('Available commands:');
      addToTerminal('  load <model>  - Load a model (llama3, mistral, phi3)');
      addToTerminal('  unload <model> - Unload a model');
      addToTerminal('  clear - Clear the terminal');
      addToTerminal('  pipeline run - Run a pipeline with current models');
      addToTerminal('  cache stats - Show cache statistics');
      addToTerminal('  cache clear - Clear the cache');
    } else if (command === 'clear') {
      setTerminalOutput([]);
    } else if (command === 'pipeline run') {
      runPipeline();
    } else if (command === 'cache stats') {
      showCacheStats();
    } else if (command === 'cache clear') {
      clearCache();
    } else {
      addToTerminal(`Command not recognized: ${command}`);
      addToTerminal('Type "help" for available commands');
    }
    
    setTerminalInput('');
  };

  // Function to run a pipeline
  const runPipeline = () => {
    // Check if any models are loaded
    const loadedModels = Object.entries(modelsLoaded).filter(([_, loaded]) => loaded);
    if (loadedModels.length === 0) {
      addToTerminal('[Pipeline] Error: No models loaded. Please load at least one model.');
      return;
    }

    setPipelineRunning(true);
    addToTerminal('[Pipeline] Starting pipeline execution...');

    // Create pipeline steps based on loaded models
    const steps = [];
    
    if (modelsLoaded.llama3) {
      steps.push({ name: 'economic_analysis', model: 'llama3', dependencies: [] });
    }
    
    if (modelsLoaded.mistral) {
      steps.push({ name: 'social_analysis', model: 'mistral', dependencies: [] });
    }
    
    if (modelsLoaded.phi3 && modelsLoaded.llama3) {
      steps.push({ name: 'integration', model: 'phi3', dependencies: ['economic_analysis'] });
    } else if (modelsLoaded.phi3 && modelsLoaded.mistral) {
      steps.push({ name: 'integration', model: 'phi3', dependencies: ['social_analysis'] });
    } else if (modelsLoaded.phi3 && modelsLoaded.llama3 && modelsLoaded.mistral) {
      steps.push({ name: 'integration', model: 'phi3', dependencies: ['economic_analysis', 'social_analysis'] });
    }
    
    setPipelineSteps(steps);
    
    // Simulate pipeline execution
    const executePipeline = async () => {
      // Execute each step in sequence, respecting dependencies
      const results = {};
      
      for (const step of steps) {
        const dependencies = step.dependencies;
        const dependenciesMet = dependencies.every(dep => results[dep]);
        
        if (dependenciesMet) {
          addToTerminal(`[Pipeline] Executing step: ${step.name} with model ${step.model}...`);
          
          // Simulate step execution time
          await new Promise(resolve => setTimeout(resolve, 1500));
          
          // Randomly introduce an error for demonstration
          if (Math.random() < 0.2 && step.model !== 'llama3') {
            addToTerminal(`[Pipeline] Error in step ${step.name}: Connection timeout`);
            addToTerminal(`[Pipeline] Attempting retry with fallback model...`);
            
            setErrorState({
              hasError: true,
              model: step.model,
              attempts: 1
            });
            
            // Simulate fallback to llama3
            await new Promise(resolve => setTimeout(resolve, 1000));
            addToTerminal(`[Pipeline] Fallback to llama3 successful`);
            
            results[step.name] = { 
              status: 'success', 
              model: 'llama3' // Fallback model
            };
            
            // Reset error state
            setTimeout(() => {
              setErrorState({
                hasError: false,
                model: '',
                attempts: 0
              });
            }, 2000);
          } else {
            // Success path
            results[step.name] = { 
              status: 'success', 
              model: step.model 
            };
            
            // Update cache stats
            setCacheStats(prev => ({
              ...prev,
              totalEntries: prev.totalEntries + 1,
              misses: prev.misses + 1,
              totalSize: `${parseInt(prev.totalSize) + 15} KB`
            }));
            
            addToTerminal(`[Pipeline] Step ${step.name} completed successfully`);
          }
        } else {
          addToTerminal(`[Pipeline] Cannot execute step ${step.name}: dependencies not met`);
        }
      }
      
      // Pipeline completion
      const successCount = Object.values(results).filter(r => r.status === 'success').length;
      addToTerminal(`[Pipeline] Pipeline execution completed. Success rate: ${successCount}/${steps.length}`);
      setPipelineRunning(false);
    };
    
    executePipeline();
  };

  // Function to show cache statistics
  const showCacheStats = () => {
    addToTerminal('[Cache] Current statistics:');
    addToTerminal(`[Cache] Total entries: ${cacheStats.totalEntries}`);
    addToTerminal(`[Cache] Cache hits: ${cacheStats.hits}`);
    addToTerminal(`[Cache] Cache misses: ${cacheStats.misses}`);
    addToTerminal(`[Cache] Total size: ${cacheStats.totalSize}`);
  };

  // Function to clear cache
  const clearCache = () => {
    addToTerminal('[Cache] Clearing cache...');
    setTimeout(() => {
      setCacheStats({
        hits: 0,
        misses: 0,
        totalEntries: 0,
        totalSize: '0 KB'
      });
      addToTerminal('[Cache] Cache cleared successfully');
    }, 800);
  };

  // Generate a simulated response
  const simulateResponse = (prompt) => {
    // Increment cache hit
    setCacheStats(prev => ({
      ...prev,
      hits: prev.hits + 1,
    }));
    
    if (prompt.includes('economic')) {
      return {
        response: "AI will transform economic sectors through automation, efficiency improvements, and new business models.",
        execution_time: 0.75
      };
    } else if (prompt.includes('social')) {
      return {
        response: "The social impact of AI includes workforce changes, privacy considerations, and ethical challenges.",
        execution_time: 0.82
      };
    } else {
      return {
        response: "AI integration across sectors will require careful governance and ethical frameworks.",
        execution_time: 0.93
      };
    }
  };

  // Live demo simulation
  const runLiveDemo = async () => {
    setTerminalOutput([]);
    addToTerminal("[PASTURE Demo] Starting live demonstration...");
    
    // Step 1: Load models
    addToTerminal("[PASTURE Demo] Step 1: Loading models...");
    setModelsLoaded({ llama3: false, mistral: false, phi3: false });
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    addToTerminal("[ModelManager] Loading model: llama3...");
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    setModelsLoaded(prev => ({ ...prev, llama3: true }));
    addToTerminal("[ModelManager] Model llama3 loaded successfully");
    
    await new Promise(resolve => setTimeout(resolve, 800));
    addToTerminal("[ModelManager] Loading model: mistral...");
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    setModelsLoaded(prev => ({ ...prev, mistral: true }));
    addToTerminal("[ModelManager] Model mistral loaded successfully");
    
    // Step 2: Create pipeline
    await new Promise(resolve => setTimeout(resolve, 1000));
    addToTerminal("[PASTURE Demo] Step 2: Creating pipeline...");
    addToTerminal("[Pipeline] Defining pipeline steps:");
    addToTerminal("  - economic_analysis: Uses llama3 to analyze economic impact");
    addToTerminal("  - social_analysis: Uses mistral to analyze social implications");
    addToTerminal("  - integration: Combines analyses into comprehensive report");
    
    const steps = [
      { name: 'economic_analysis', model: 'llama3', dependencies: [] },
      { name: 'social_analysis', model: 'mistral', dependencies: [] },
      { name: 'integration', model: 'llama3', dependencies: ['economic_analysis', 'social_analysis'] }
    ];
    
    setPipelineSteps(steps);
    
    // Step 3: Execute pipeline
    await new Promise(resolve => setTimeout(resolve, 1500));
    addToTerminal("[PASTURE Demo] Step 3: Executing pipeline...");
    setPipelineRunning(true);
    
    // Economic analysis
    addToTerminal("[Pipeline] Executing step: economic_analysis with model llama3...");
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Check cache first
    addToTerminal("[Cache] Checking cache for economic_analysis...");
    await new Promise(resolve => setTimeout(resolve, 600));
    addToTerminal("[Cache] Cache miss. Executing model...");
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    addToTerminal("[Pipeline] Step economic_analysis completed successfully");
    setCacheStats(prev => ({
      ...prev,
      misses: prev.misses + 1,
      totalEntries: prev.totalEntries + 1,
      totalSize: `${parseInt(prev.totalSize || 0) + 15} KB`
    }));
    
    // Social analysis
    await new Promise(resolve => setTimeout(resolve, 800));
    addToTerminal("[Pipeline] Executing step: social_analysis with model mistral...");
    
    // Simulate error
    await new Promise(resolve => setTimeout(resolve, 1500));
    addToTerminal("[Pipeline] Error in step social_analysis: Connection timeout");
    setErrorState({
      hasError: true,
      model: 'mistral',
      attempts: 1
    });
    
    // Retry logic
    addToTerminal("[Pipeline] Retry attempt 1 of 3...");
    await new Promise(resolve => setTimeout(resolve, 1000));
    addToTerminal("[Pipeline] Error persists, falling back to llama3...");
    
    await new Promise(resolve => setTimeout(resolve, 1200));
    addToTerminal("[Pipeline] Fallback to llama3 successful");
    addToTerminal("[Pipeline] Step social_analysis completed with fallback model");
    
    // Reset error state
    setErrorState({
      hasError: false,
      model: '',
      attempts: 0
    });
    
    // Integration step
    await new Promise(resolve => setTimeout(resolve, 1000));
    addToTerminal("[Pipeline] Executing step: integration with model llama3...");
    await new Promise(resolve => setTimeout(resolve, 2000));
    addToTerminal("[Pipeline] Step integration completed successfully");
    setCacheStats(prev => ({
      ...prev,
      misses: prev.misses + 1,
      totalEntries: prev.totalEntries + 1,
      totalSize: `${parseInt(prev.totalSize || 0) + 25} KB`
    }));
    
    // Pipeline completion
    await new Promise(resolve => setTimeout(resolve, 800));
    addToTerminal("[Pipeline] Pipeline execution completed. Success rate: 3/3");
    setPipelineRunning(false);
    
    // Show final results
    await new Promise(resolve => setTimeout(resolve, 1000));
    addToTerminal("[PASTURE Demo] Live demonstration completed!");
    addToTerminal("[PASTURE Demo] Type 'help' to explore more commands");
  };

  // Tab content rendering
  const renderTabContent = () => {
    switch(activeTab) {
      case 'overview':
        return (
          <div className="p-4 space-y-4">
            <h2 className="font-bold text-xl text-green-400">What is PASTURE?</h2>
            <p className="text-green-300">
              PASTURE (Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement) is a middleware framework designed to orchestrate multiple AI models hosted on Ollama. It enables seamless communication between different LLMs while ensuring robust error handling, response validation, and high reliability.
            </p>
            
            <div className="my-6 p-3 bg-black border border-pink-500 rounded text-green-400 font-mono">
              <p className="whitespace-pre">
                {`        ___         ___           ___                       ___           ___           ___     
       /  /\\       /  /\\         /  /\\          ___        /__/\\         /  /\\         /  /\\    
      /  /::\\     /  /::\\       /  /:/_        /  /\\       \\  \\:\\       /  /::\\       /  /:/_   
     /  /:/\\:\\   /  /:/\\:\\     /  /:/ /\\      /  /:/        \\  \\:\\     /  /:/\\:\\     /  /:/ /\\  
    /  /:/~/:/  /  /:/~/::\\   /  /:/ /::\\    /  /:/     ___  \\  \\:\\   /  /:/~/:/    /  /:/ /:/_ 
   /__/:/ /:/  /__/:/ /:/\\:\\ /__/:/ /:/\\:\\  /  /::\\    /__/\\  \\__\\:\\ /__/:/ /:/___ /__/:/ /:/ /\\
   \\  \\:\\/:/   \\  \\:\\/:/__\\/ \\  \\:\\/:/~/:/ /__/:/\\:\\   \\  \\:\\ /  /:/ \\  \\:\\/:::::/ \\  \\:\\/:/ /:/
    \\  \\::/     \\  \\::/       \\  \\::/ /:/  \\__\\/  \\:\\   \\  \\:\\  /:/   \\  \\::/~~~~   \\  \\::/ /:/ 
     \\  \\:\\      \\  \\:\\        \\__\\/ /:/        \\  \\:\\   \\  \\:\\/:/     \\  \\:\\        \\  \\:\\/:/  
      \\  \\:\\      \\  \\:\\         /__/:/          \\__\\/    \\  \\::/       \\  \\:\\        \\  \\::/   
       \\__\\/       \\__\\/         \\__\\/                     \\__\\/         \\__\\/         \\__\\/    `}
              </p>
            </div>
            
            <h3 className="font-bold text-xl text-pink-400 mt-6">Key Features</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3 border border-pink-500 rounded">
                <h4 className="font-bold text-pink-400">Model Management</h4>
                <ul className="list-disc list-inside text-green-300">
                  <li>Sequential loading to prevent memory issues</li>
                  <li>Health checks for model verification</li>
                  <li>Resource management for efficient memory usage</li>
                  <li>Automatic fallbacks when models fail</li>
                </ul>
              </div>
              
              <div className="p-3 border border-pink-500 rounded">
                <h4 className="font-bold text-pink-400">Error Resilience</h4>
                <ul className="list-disc list-inside text-green-300">
                  <li>Configurable exponential backoff</li>
                  <li>Classification of recoverable errors</li>
                  <li>Circuit breaking for failing models</li>
                  <li>Response quality validation</li>
                </ul>
              </div>
              
              <div className="p-3 border border-pink-500 rounded">
                <h4 className="font-bold text-pink-400">JSON Processing</h4>
                <ul className="list-disc list-inside text-green-300">
                  <li>Automatic JSON format repair</li>
                  <li>Schema validation for outputs</li>
                  <li>Structured data extraction</li>
                </ul>
              </div>
              
              <div className="p-3 border border-pink-500 rounded">
                <h4 className="font-bold text-pink-400">Pipeline Architecture</h4>
                <ul className="list-disc list-inside text-green-300">
                  <li>Step dependencies for complex workflows</li>
                  <li>Controlled execution flow</li>
                  <li>Result aggregation across models</li>
                  <li>Detailed performance metrics</li>
                </ul>
              </div>
            </div>
            
            <div className="mt-8 text-center">
              <button 
                onClick={() => setActiveTab('interactive')}
                className="px-6 py-3 bg-pink-600 hover:bg-pink-700 text-white rounded font-bold shadow-lg hover:shadow-pink-500/20 transition-all"
              >
                Try Interactive Demo
              </button>
            </div>
          </div>
        );
        
      case 'model-management':
        return (
          <div className="p-4">
            <h2 className="font-bold text-xl text-green-400 mb-4">Model Management</h2>
            <p className="text-green-300 mb-6">
              PASTURE intelligently manages the loading, unloading, and health checking of models to prevent memory issues and ensure reliable operation.
            </p>
            
            <div className="border border-pink-500 rounded p-4 mb-6">
              <h3 className="text-pink-400 font-bold mb-2">Available Models</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(modelsLoaded).map(([model, loaded]) => (
                  <div key={model} className="border border-green-500 rounded p-3 flex flex-col items-center">
                    <div className={`w-4 h-4 rounded-full ${loaded ? 'bg-green-500' : 'bg-red-500'} mb-2`}></div>
                    <div className="text-green-300 font-bold">{model}</div>
                    <div className="text-green-400 text-sm">{loaded ? 'Loaded' : 'Not Loaded'}</div>
                    <div className="mt-2 flex space-x-2">
                      <button
                        onClick={() => loadModel(model)}
                        disabled={loaded}
                        className={`px-3 py-1 text-xs rounded ${loaded ? 'bg-gray-700 text-gray-500' : 'bg-green-700 hover:bg-green-800 text-white'}`}
                      >
                        Load
                      </button>
                      <button
                        onClick={() => unloadModel(model)}
                        disabled={!loaded}
                        className={`px-3 py-1 text-xs rounded ${!loaded ? 'bg-gray-700 text-gray-500' : 'bg-red-700 hover:bg-red-800 text-white'}`}
                      >
                        Unload
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Health Checks</h3>
                <p className="text-green-300 text-sm mb-3">
                  PASTURE regularly checks model health to ensure they're responsive and functioning correctly.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Model health check example
async def check_model_health(model_name: str) -> bool:
    """Check if a model is healthy and responsive"""
    status = self._get_model_status(model_name)
    
    # Try a minimal request to the model
    result = await self._request("generate", {
        "model": model_name,
        "prompt": "Hello",
        "stream": False
    })
    
    # Update status tracking
    status.last_checked = time.time()
    
    if "error" in result:
        self._increment_failure_count(model_name)
        return False
            
    return True`}</pre>
                </div>
              </div>
              
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Fallback Mechanism</h3>
                <p className="text-green-300 text-sm mb-3">
                  When a model fails, PASTURE automatically tries alternative models based on intelligent selection.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Fallback example
async def get_fallback(self, data: Dict[str, Any]) -> Dict:
    """Try fallback models when primary model fails"""
    # Get alternatives
    if self.fallback_models:
        fallback_candidates = self.fallback_models
    else:
        available_models = await self.model_manager.get_available_models()
        fallback_model = await self.model_manager.get_fallback_model(
            self.model_name, available_models
        )
        fallback_candidates = [fallback_model] if fallback_model else []
    
    for fallback_model in fallback_candidates:
        # Try each fallback
        result = await self.model_manager.generate_with_model(
            fallback_model, prompt, self.options
        )
        
        if "error" not in result:
            return {
                "output": result,
                "model": fallback_model,
                "status": "success",
                "fallback": True
            }
            
    # All fallbacks failed
    return {"error": "all_models_failed"}`}</pre>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'pipeline':
        return (
          <div className="p-4">
            <h2 className="font-bold text-xl text-green-400 mb-4">Pipeline Architecture</h2>
            <p className="text-green-300 mb-6">
              PASTURE's pipeline architecture allows you to define complex workflows with dependencies between steps, each potentially using different models.
            </p>
            
            <div className="border border-pink-500 rounded p-4 mb-6">
              <h3 className="text-pink-400 font-bold mb-2">Pipeline Visualization</h3>
              
              <div className="overflow-auto">
                <div className="min-w-[600px]">
                  <div className="py-8 relative">
                    {/* Pipeline step boxes */}
                    <div className="flex justify-between">
                      <div className="flex space-x-4">
                        <div className={`w-48 h-32 border-2 ${modelsLoaded.llama3 ? 'border-green-500' : 'border-gray-700'} rounded p-2 flex flex-col items-center justify-center`}>
                          <div className="text-pink-400 font-bold mb-2">Economic Analysis</div>
                          <div className="text-green-300">Model: llama3</div>
                          <div className="text-green-300 text-sm">Dependencies: None</div>
                          <div className={`w-3 h-3 rounded-full mt-2 ${modelsLoaded.llama3 ? 'bg-green-500' : 'bg-red-500'}`}></div>
                        </div>
                        
                        <div className={`w-48 h-32 border-2 ${modelsLoaded.mistral ? 'border-green-500' : 'border-gray-700'} rounded p-2 flex flex-col items-center justify-center`}>
                          <div className="text-pink-400 font-bold mb-2">Social Analysis</div>
                          <div className="text-green-300">Model: mistral</div>
                          <div className="text-green-300 text-sm">Dependencies: None</div>
                          <div className={`w-3 h-3 rounded-full mt-2 ${modelsLoaded.mistral ? 'bg-green-500' : 'bg-red-500'}`}></div>
                        </div>
                      </div>
                      
                      <div className={`w-48 h-32 border-2 ${modelsLoaded.phi3 ? 'border-green-500' : 'border-gray-700'} rounded p-2 flex flex-col items-center justify-center`}>
                        <div className="text-pink-400 font-bold mb-2">Integration</div>
                        <div className="text-green-300">Model: phi3</div>
                        <div className="text-green-300 text-sm">Dependencies: Economic, Social</div>
                        <div className={`w-3 h-3 rounded-full mt-2 ${modelsLoaded.phi3 ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      </div>
                    </div>
                    
                    {/* Dependency arrows using SVG for better control */}
                    <svg className="absolute top-0 left-0 w-full h-full pointer-events-none" style={{ zIndex: -1 }}>
                      <defs>
                        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                          <polygon points="0 0, 10 3.5, 0 7" fill="#ec4899" />
                        </marker>
                      </defs>
                      
                      {/* Lines connecting models */}
                      <line x1="160" y1="80" x2="400" y2="80" stroke="#ec4899" strokeWidth="2" markerEnd="url(#arrowhead)" />
                      <line x1="350" y1="80" x2="400" y2="80" stroke="#ec4899" strokeWidth="2" markerEnd="url(#arrowhead)" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 text-center">
                <button
                  onClick={runPipeline}
                  disabled={pipelineRunning || Object.values(modelsLoaded).every(loaded => !loaded)}
                  className={`px-4 py-2 rounded font-bold ${pipelineRunning || Object.values(modelsLoaded).every(loaded => !loaded) ? 'bg-gray-700 text-gray-500' : 'bg-pink-600 hover:bg-pink-700 text-white'}`}
                >
                  {pipelineRunning ? 'Running Pipeline...' : 'Run Pipeline'}
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Pipeline Configuration</h3>
                <p className="text-green-300 text-sm mb-3">
                  Define complex workflows with dependencies between steps.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Define pipeline steps
pipeline = Pipeline(
    steps=[
        ("economic", economic_step, []),  # No dependencies
        ("social", social_step, []),      # No dependencies
        ("integration", integration_step, 
          ["economic", "social"])  # Depends on both analyses
    ],
    config=config
)

# Run the pipeline
results = await pipeline.run({
    "query": "Impact of AI on society"
})`}</pre>
                </div>
              </div>
              
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Pipeline Execution</h3>
                <p className="text-green-300 text-sm mb-3">
                  PASTURE handles step order, dependency resolution, and error recovery.
                </p>
                
                {/* Live execution status */}
                <div className="bg-black border border-green-500 rounded p-3">
                  <div className="mb-2 text-green-400 font-bold">Execution Status:</div>
                  {pipelineSteps.length === 0 ? (
                    <div className="text-green-300 italic">No pipeline defined. Load models first.</div>
                  ) : (
                    <div className="space-y-2">
                      {pipelineSteps.map((step) => (
                        <div key={step.name} className="flex items-center">
                          <div className={`w-3 h-3 rounded-full ${pipelineRunning ? 'bg-yellow-500' : 'bg-green-500'} mr-2`}></div>
                          <div className="text-green-300">{step.name} ({step.model})</div>
                          {errorState.hasError && errorState.model === step.model && (
                            <div className="ml-2 text-red-500 text-xs">Error - Retrying...</div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'caching':
        return (
          <div className="p-4">
            <h2 className="font-bold text-xl text-green-400 mb-4">Caching System</h2>
            <p className="text-green-300 mb-6">
              PASTURE includes a robust caching system to avoid redundant API calls, improve performance, and reduce costs.
            </p>
            
            <div className="border border-pink-500 rounded p-4 mb-6">
              <h3 className="text-pink-400 font-bold mb-2">Cache Statistics</h3>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="border border-green-500 rounded p-3 flex flex-col items-center">
                  <div className="text-green-400 font-bold mb-1">Total Entries</div>
                  <div className="text-pink-400 text-2xl font-bold">{cacheStats.totalEntries}</div>
                </div>
                
                <div className="border border-green-500 rounded p-3 flex flex-col items-center">
                  <div className="text-green-400 font-bold mb-1">Cache Hits</div>
                  <div className="text-pink-400 text-2xl font-bold">{cacheStats.hits}</div>
                </div>
                
                <div className="border border-green-500 rounded p-3 flex flex-col items-center">
                  <div className="text-green-400 font-bold mb-1">Cache Misses</div>
                  <div className="text-pink-400 text-2xl font-bold">{cacheStats.misses}</div>
                </div>
                
                <div className="border border-green-500 rounded p-3 flex flex-col items-center">
                  <div className="text-green-400 font-bold mb-1">Cache Size</div>
                  <div className="text-pink-400 text-2xl font-bold">{cacheStats.totalSize}</div>
                </div>
              </div>
              
              <div className="mt-4 flex space-x-4 justify-center">
                <button
                  onClick={() => {
                    // Simulate cache hit
                    const prompt = "Analyze the economic impact of AI";
                    const response = simulateResponse(prompt);
                    addToTerminal(`[Cache] Hit for: "${prompt.substring(0, 25)}..."`);
                    addToTerminal(`[Cache] Returned cached response in 0.01s`);
                  }}
                  className="px-4 py-2 bg-green-700 hover:bg-green-800 text-white rounded font-bold"
                >
                  Simulate Cache Hit
                </button>
                
                <button
                  onClick={clearCache}
                  className="px-4 py-2 bg-red-700 hover:bg-red-800 text-white rounded font-bold"
                >
                  Clear Cache
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Cache Implementation</h3>
                <p className="text-green-300 text-sm mb-3">
                  PASTURE uses a file-based cache with TTL (Time-To-Live) support.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Cache implementation example
class FileCache:
    """File-based cache with TTL support"""
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with error handling"""
        try:
            file_path = self._cache_dir / f"{self._hash_key(key)}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    entry = CacheEntry(**data)
                    
                    # Check if expired
                    if (entry.expires_at is not None and 
                        entry.expires_at < time.time()):
                        return None
                        
                    logger.debug(f"Cache hit for {key}")
                    return entry.value
            
            logger.debug(f"Cache miss for {key}")
            return None
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
            return None`}</pre>
                </div>
              </div>
              
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Using the Cache</h3>
                <p className="text-green-300 text-sm mb-3">
                  How to leverage PASTURE's caching system in your application.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Using cache with different TTL values
# Initialize cache
cache = FileCache("./my_cache_dir")

# Set response with 1 hour TTL
await cache.set(key, response, ttl=3600)

# Set response with 1 day TTL
await cache.set(key, response, ttl=86400)

# Cache indefinitely
await cache.set(key, response, ttl=None)

# Get cache statistics
stats = await cache.get_stats()
print(f"Active entries: {stats['active_entries']}")
print(f"Cache size: {stats['cache_size_bytes']} bytes")

# Clear specific entries or entire cache
await cache.clear("specific_key")  # Clear one entry
await cache.clear()                # Clear all entries`}</pre>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'error-resilience':
        return (
          <div className="p-4">
            <h2 className="font-bold text-xl text-green-400 mb-4">Error Resilience</h2>
            <p className="text-green-300 mb-6">
              PASTURE provides robust error handling with automatic retries, fallbacks, and circuit breaking to ensure your AI pipelines remain operational even when models fail.
            </p>
            
            <div className="border border-pink-500 rounded p-4 mb-6">
              <h3 className="text-pink-400 font-bold mb-2">Error Handling Visualization</h3>
              
              <div className="relative h-64 border border-green-500 rounded p-4">
                {/* Error state visualization */}
                <div className={`absolute inset-0 flex items-center justify-center bg-black bg-opacity-70 transition-opacity duration-500 ${errorState.hasError ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
                  <div className="text-center">
                    <div className="text-red-500 font-bold text-xl mb-2">Model Error Detected</div>
                    <div className="text-pink-400">Model: {errorState.model}</div>
                    <div className="text-green-300 mb-4">Attempt: {errorState.attempts} of 3</div>
                    <div className="animate-pulse text-green-400">Initiating fallback strategy...</div>
                  </div>
                </div>
                
                {/* Normal state */}
                <div className={`transition-opacity duration-500 ${errorState.hasError ? 'opacity-0' : 'opacity-100'}`}>
                  <div className="text-center mb-6">
                    <button
                      onClick={() => {
                        setErrorState({
                          hasError: true,
                          model: 'mistral',
                          attempts: 1
                        });
                        
                        addToTerminal('[Error Simulation] Error detected in model: mistral');
                        addToTerminal('[Error Simulation] Error type: connection_timeout');
                        addToTerminal('[Error Simulation] Initiating retry with exponential backoff...');
                        
                        setTimeout(() => {
                          addToTerminal('[Error Simulation] Retry 1 failed, increasing backoff...');
                          setErrorState(prev => ({...prev, attempts: 2}));
                          
                          setTimeout(() => {
                            addToTerminal('[Error Simulation] Retry 2 failed, falling back to alternative model');
                            addToTerminal('[Error Simulation] Switching to fallback model: llama3');
                            
                            setTimeout(() => {
                              addToTerminal('[Error Simulation] Fallback successful! Continuing pipeline execution');
                              setErrorState({
                                hasError: false,
                                model: '',
                                attempts: 0
                              });
                            }, 1500);
                          }, 1500);
                        }, 1500);
                      }}
                      className="px-4 py-2 bg-red-700 hover:bg-red-800 text-white rounded font-bold"
                    >
                      Simulate Error
                    </button>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="border border-green-500 rounded p-2 text-center">
                      <div className="text-pink-400 font-bold">Retry Logic</div>
                      <div className="text-green-300 text-sm">Exponential backoff with configurable attempts</div>
                    </div>
                    
                    <div className="border border-green-500 rounded p-2 text-center">
                      <div className="text-pink-400 font-bold">Error Classification</div>
                      <div className="text-green-300 text-sm">Separate recoverable from fatal errors</div>
                    </div>
                    
                    <div className="border border-green-500 rounded p-2 text-center">
                      <div className="text-pink-400 font-bold">Model Fallbacks</div>
                      <div className="text-green-300 text-sm">Automatic switching to alternative models</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Retry Configuration</h3>
                <p className="text-green-300 text-sm mb-3">
                  Configure retry behavior with different strategies and parameters.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Configure retry behavior
retry_config = RetryConfig(
    max_attempts=3,
    strategy=RetryStrategy.EXPONENTIAL,
    min_wait=1.0,  # Initial wait in seconds
    max_wait=30.0  # Maximum wait in seconds
)

# Implementing retry decorator
@retry(
    stop_after_attempt=retry_config.max_attempts,
    wait_exponential(
        multiplier=1, 
        min=retry_config.min_wait, 
        max=retry_config.max_wait
    ),
    retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
    before_sleep_log(logger, logging.WARNING)
)
async def _request(self, endpoint, json_data):
    # Implementation here
    ...`}</pre>
                </div>
              </div>
              
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Circuit Breaking</h3>
                <p className="text-green-300 text-sm mb-3">
                  PASTURE automatically disables consistently failing models.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`# Circuit breaking implementation
def _increment_failure_count(self, model_name: str) -> None:
    """Increment failure count and check threshold"""
    status = self._get_model_status(model_name)
    status.failure_count += 1
    
    # Mark as unhealthy if failure count exceeds threshold
    if status.failure_count >= self.config.fallback_threshold:
        status.healthy = False
        logger.warning(
            f"Model {model_name} marked unhealthy after "
            f"{status.failure_count} failures"
        )
        
# When using the model
if not model_status.healthy:
    logger.warning(f"Circuit breaker open for {model_name}")
    return await self.get_fallback(data)`}</pre>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'live-demo':
        return (
          <div className="p-4">
            <h2 className="font-bold text-xl text-green-400 mb-4">Live PASTURE Demo</h2>
            <p className="text-green-300 mb-6">
              Watch PASTURE in action with this automated demonstration of a complete pipeline execution.
            </p>
            
            <div className="border border-pink-500 rounded p-4 mb-6">
              <h3 className="text-pink-400 font-bold mb-2">AI Impact Analysis Pipeline</h3>
              <p className="text-green-300 mb-4">
                This demo shows a complete pipeline that analyzes the impact of AI from economic and social perspectives, then integrates the findings into a comprehensive report.
              </p>
              
              <div className="flex justify-center mb-4">
                <button
                  onClick={runLiveDemo}
                  disabled={pipelineRunning}
                  className={`px-6 py-3 rounded font-bold ${pipelineRunning ? 'bg-gray-700 text-gray-500' : 'bg-pink-600 hover:bg-pink-700 text-white'}`}
                >
                  {pipelineRunning ? 'Demo Running...' : 'Start Live Demo'}
                </button>
              </div>
              
              <div className="bg-black border border-green-500 rounded p-2 h-64 overflow-auto font-mono text-sm" ref={terminalRef}>
                {terminalOutput.length === 0 ? (
                  <div className="text-green-400 p-2">Press "Start Live Demo" to begin the demonstration...</div>
                ) : (
                  <div className="p-2">
                    {terminalOutput.map((line, i) => (
                      <div key={i} className={line.includes('Error') ? 'text-red-400' : 'text-green-400'}>
                        {line}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Pipeline Structure</h3>
                <p className="text-green-300 text-sm mb-3">
                  This demo uses a 3-step pipeline with two parallel initial analyses and a final integration step.
                </p>
                <div className="bg-black border border-green-500 rounded p-3">
                  <div className="flex flex-col items-center mb-4">
                    <div className="w-full flex justify-between items-center mb-4">
                      <div className="w-40 h-16 border border-green-500 rounded flex items-center justify-center">
                        <div className="text-pink-400 text-sm font-bold">Economic Analysis</div>
                      </div>
                      
                      <div className="w-40 h-16 border border-green-500 rounded flex items-center justify-center">
                        <div className="text-pink-400 text-sm font-bold">Social Analysis</div>
                      </div>
                    </div>
                    
                    <svg width="280" height="40" className="mb-2">
                      <line x1="70" y1="0" x2="140" y2="40" stroke="#ec4899" strokeWidth="2" strokeDasharray="4 2" />
                      <line x1="210" y1="0" x2="140" y2="40" stroke="#ec4899" strokeWidth="2" strokeDasharray="4 2" />
                    </svg>
                    
                    <div className="w-40 h-16 border border-green-500 rounded flex items-center justify-center">
                      <div className="text-pink-400 text-sm font-bold">Integration</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Code Sample</h3>
                <p className="text-green-300 text-sm mb-3">
                  How to implement this pipeline in your own application.
                </p>
                <div className="bg-black border border-green-500 rounded p-3 font-mono text-green-400 text-sm">
                  <pre>{`import asyncio
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

async def main():
    # Initialize
    config = Config()
    cache = FileCache(config.cache.dir)
    model_manager = ModelManager(config, cache)
    
    # Define steps
    economic_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="Analyze the economic impact of {query}.",
        options={"temperature": 0.7}
    )
    
    social_step = ModelStep(
        model_manager=model_manager,
        model_name="mistral",
        prompt_template="Analyze the social implications of {query}.",
        options={"temperature": 0.7}
    )
    
    integration_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="""
        Integrate these analyses into a comprehensive report:
        
        Topic: {query}
        
        Economic Analysis:
        {economic[response]}
        
        Social Analysis:
        {social[response]}
        """,
        options={"temperature": 0.5}
    )
    
    # Create pipeline
    pipeline = Pipeline(
        steps=[
            ("economic", economic_step, []),
            ("social", social_step, []),
            ("integration", integration_step, ["economic", "social"])
        ],
        config=config
    )
    
    # Run pipeline
    results = await pipeline.run({
        "query": "The impact of AI on society"
    })
    
    # Print final result
    print(results["results"]["integration"]["output"]["response"])`}</pre>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'interactive':
        return (
          <div className="p-4">
            <h2 className="font-bold text-xl text-green-400 mb-4">Interactive Terminal</h2>
            <p className="text-green-300 mb-6">
              Experience PASTURE through this interactive terminal. Try managing models, running pipelines, and exploring the caching system.
            </p>
            
            <div className="border border-pink-500 rounded p-4 mb-6">
              <h3 className="text-pink-400 font-bold mb-2">PASTURE Terminal</h3>
              
              <div className="bg-black border border-green-500 rounded p-2">
                <div className="font-mono text-green-400 h-64 overflow-auto mb-2" ref={terminalRef}>
                  <div className="p-2">
                    {terminalOutput.map((line, i) => (
                      <div key={i} className={
                        line.includes('Error') ? 'text-red-400' : 
                        line.startsWith('>') ? 'text-pink-400 font-bold' : 
                        'text-green-400'
                      }>
                        {line}
                      </div>
                    ))}
                  </div>
                </div>
                
                <form onSubmit={processCommand} className="flex border-t border-green-700 p-2">
                  <span className="text-pink-400 mr-2">$</span>
                  <input
                    type="text"
                    value={terminalInput}
                    onChange={(e) => setTerminalInput(e.target.value)}
                    className="bg-transparent flex-1 outline-none border-none text-green-400 font-mono focus:ring-2 focus:ring-pink-500"
                    placeholder="Type command (help, load, unload, etc.)"
                    autoFocus
                    ref={(input) => {
                      if (input && activeTab === 'interactive') {
                        setTimeout(() => input.focus(), 100);
                      }
                    }}
                  />
                  <button 
                    type="submit" 
                    className="ml-2 px-3 py-1 bg-pink-700 hover:bg-pink-600 text-white rounded text-sm"
                  >
                    Enter
                  </button>
                </form>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Available Commands</h3>
                <div className="bg-black border border-green-500 rounded p-3">
                  <table className="w-full text-green-300 text-sm">
                    <tbody>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">load &lt;model&gt;</td>
                        <td>Load a model (llama3, mistral, phi3)</td>
                      </tr>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">unload &lt;model&gt;</td>
                        <td>Unload a model</td>
                      </tr>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">pipeline run</td>
                        <td>Run a pipeline with loaded models</td>
                      </tr>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">cache stats</td>
                        <td>Show cache statistics</td>
                      </tr>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">cache clear</td>
                        <td>Clear the cache</td>
                      </tr>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">clear</td>
                        <td>Clear the terminal</td>
                      </tr>
                      <tr>
                        <td className="py-1 pr-4 text-pink-400 font-mono">help</td>
                        <td>Show available commands</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div className="border border-pink-500 rounded p-4">
                <h3 className="text-pink-400 font-bold mb-2">Learning Guide</h3>
                <p className="text-green-300 text-sm mb-3">
                  Try these steps to learn about PASTURE:
                </p>
                
                <ol className="list-decimal list-inside text-green-300 text-sm space-y-2">
                  <li>Load models with <span className="text-pink-400 font-mono">load llama3</span> and <span className="text-pink-400 font-mono">load mistral</span></li>
                  <li>Run a pipeline with <span className="text-pink-400 font-mono">pipeline run</span></li>
                  <li>Check cache statistics with <span className="text-pink-400 font-mono">cache stats</span></li>
                  <li>Run the pipeline again to see caching in action</li>
                  <li>Unload a model with <span className="text-pink-400 font-mono">unload llama3</span></li>
                  <li>Try running the pipeline with different models</li>
                  <li>Clear the cache with <span className="text-pink-400 font-mono">cache clear</span></li>
                </ol>
              </div>
            </div>
          </div>
        );
        
      default:
        return <div>Select a tab to explore PASTURE</div>;
    }
  };

  return (
    <div className="bg-black text-green-300 min-h-screen">
      <header className="bg-black border-b border-pink-500 p-4">
        <div className="font-mono text-center text-green-400 text-xs mb-2">
          <pre className="hidden md:block overflow-x-auto">
            {`        ___         ___           ___                       ___           ___           ___     
       /  /\\       /  /\\         /  /\\          ___        /__/\\         /  /\\         /  /\\    
      /  /::\\     /  /::\\       /  /:/_        /  /\\       \\  \\:\\       /  /::\\       /  /:/_   
     /  /:/\\:\\   /  /:/\\:\\     /  /:/ /\\      /  /:/        \\  \\:\\     /  /:/\\:\\     /  /:/ /\\  
    /  /:/~/:/  /  /:/~/::\\   /  /:/ /::\\    /  /:/     ___  \\  \\:\\   /  /:/~/:/    /  /:/ /:/_ 
   /__/:/ /:/  /__/:/ /:/\\:\\ /__/:/ /:/\\:\\  /  /::\\    /__/\\  \\__\\:\\ /__/:/ /:/___ /__/:/ /:/ /\\
   \\  \\:\\/:/   \\  \\:\\/:/__\\/ \\  \\:\\/:/~/:/ /__/:/\\:\\   \\  \\:\\ /  /:/ \\  \\:\\/:::::/ \\  \\:\\/:/ /:/
    \\  \\::/     \\  \\::/       \\  \\::/ /:/  \\__\\/  \\:\\   \\  \\:\\  /:/   \\  \\::/~~~~   \\  \\::/ /:/ 
     \\  \\:\\      \\  \\:\\        \\__\\/ /:/        \\  \\:\\   \\  \\:\\/:/     \\  \\:\\        \\  \\:\\/:/  
      \\  \\:\\      \\  \\:\\         /__/:/          \\__\\/    \\  \\::/       \\  \\:\\        \\  \\::/   
       \\__\\/       \\__\\/         \\__\\/                     \\__\\/         \\__\\/         \\__\\/    `}
          </pre>
          <div className="md:hidden text-2xl font-bold text-green-400">PASTURE</div>
        </div>
        <h1 className="text-2xl md:text-3xl text-center font-bold text-pink-400">
          Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement
        </h1>
        <div className="text-center text-green-300 mt-2">
          A cyberpunk middleware solution for orchestrating LLMs with reliability and style
        </div>
      </header>
      
      <nav className="bg-gray-900 border-b border-pink-500 overflow-x-auto">
        <div className="flex space-x-1 p-1">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'overview' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('model-management')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'model-management' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors`}
          >
            Model Management
          </button>
          <button
            onClick={() => setActiveTab('pipeline')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'pipeline' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors`}
          >
            Pipeline Architecture
          </button>
          <button
            onClick={() => setActiveTab('error-resilience')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'error-resilience' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors`}
          >
            Error Resilience
          </button>
          <button
            onClick={() => setActiveTab('caching')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'caching' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors`}
          >
            Caching System
          </button>
          <button
            onClick={() => setActiveTab('live-demo')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'live-demo' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors`}
          >
            Live Demo
          </button>
          <button
            onClick={() => setActiveTab('interactive')}
            className={`px-3 py-2 whitespace-nowrap ${activeTab === 'interactive' ? 'bg-pink-900 text-pink-400' : 'text-green-400 hover:bg-gray-800'} rounded-t-md transition-colors flex items-center`}
          >
            <Terminal size={16} className="mr-1" />
            Interactive Terminal
          </button>
        </div>
      </nav>
      
      <main>
        {renderTabContent()}
      </main>
      
      <footer className="bg-black border-t border-pink-500 p-4 text-center text-green-300 text-sm">
        <div>PASTURE Framework - A Middleware Solution for Model Orchestration</div>
        <div className="text-pink-400 mt-1">The Greatest things built, often have yet to be built</div>
      </footer>
    </div>
  );
};

export default PastureDemo;
