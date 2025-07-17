#!/usr/bin/env python3
"""
Enhanced ALLA Arc Solver - Main Script
Human-level cognitive architecture for ARC-2 task solving
"""

import json
import numpy as np
import os
import time
import logging
from pathlib import Path

import re

# Remove emojis from log messages
def strip_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

class EmojiStripFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        return strip_emojis(msg)

# Configure logging with UTF-8 encoding and emoji stripping
formatter = EmojiStripFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Create handlers with the custom formatter
file_handler = logging.FileHandler('enhanced_alla_run.log', encoding='utf-8')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

def run_enhanced_alla_on_arc_dataset():
    """Run Enhanced ALLA on the complete ARC dataset"""
    
    try:
        from enhanced_alla_arc_system import EnhancedALLASystem
        
        # Initialize the Enhanced ALLA system
        logger.info("Initializing Enhanced ALLA Cognitive Architecture...")
        alla_system = EnhancedALLASystem(data_path="d:/DARWIN/ARC-AGI-2/data/training")
        
        # Get all ARC task files
        task_files = list(Path("d:/DARWIN/ARC-AGI-2/data/training").glob("*.json"))
        logger.info(f"Found {len(task_files)} ARC training tasks")
        
        # Process tasks in batches for better learning
        batch_size = 10
        total_batches = (len(task_files) + batch_size - 1) // batch_size
        
        all_results = []
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, len(task_files))
            batch_files = task_files[start_idx:end_idx]
            
            logger.info(f"Processing batch {batch_idx + 1}/{total_batches} ({len(batch_files)} tasks)")
            
            batch_results = []
            
            # Process each task in the batch
            for task_file in batch_files:
                try:
                    logger.info(f"Processing {task_file.name}")
                    result = alla_system.process_arc_task(str(task_file))
                    batch_results.append(result)
                    
                    # Log task result
                    status = "SUCCESS" if result.success else "FAILED"
                    logger.info(f"{status} {task_file.name}: {result.accuracy:.2%} accuracy, {result.confidence:.2f} confidence")
                    
                except Exception as e:
                    logger.error(f"Error processing {task_file.name}: {e}")
                    continue
            
            all_results.extend(batch_results)
            
            # Evolve learning strategies after each batch
            if len(all_results) >= 10:
                logger.info("Evolving learning strategies...")
                evolution_results = alla_system.evolve_learning_strategies()
                logger.info(f"Strategy evolution complete: {len(evolution_results)} improvements")
            
            # Generate progress report
            if len(all_results) > 0:
                success_rate = sum(1 for r in all_results if r.success) / len(all_results)
                avg_accuracy = sum(r.accuracy for r in all_results) / len(all_results)
                avg_confidence = sum(r.confidence for r in all_results) / len(all_results)
                
                logger.info(f"Progress Report - Batch {batch_idx + 1}:")
                logger.info(f"   Success Rate: {success_rate:.2%}")
                logger.info(f"   Average Accuracy: {avg_accuracy:.2%}")
                logger.info(f"   Average Confidence: {avg_confidence:.2f}")
        
        # Generate comprehensive final report
        logger.info("Generating comprehensive learning report...")
        final_report = alla_system.generate_comprehensive_learning_report()
        
        # Save detailed results
        save_enhanced_results(all_results, final_report)
        
        # Print final summary
        print_final_summary(all_results, final_report)
        
        return all_results, final_report
        
    except Exception as e:
        logger.error(f"Critical error in Enhanced ALLA execution: {e}")
        raise

def save_enhanced_results(results, final_report):
    """Save Enhanced ALLA results and reports"""
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Custom JSON encoder for complex objects
    def json_serializer(obj):
        if isinstance(obj, bool):
            return bool(obj)
        elif isinstance(obj, (int, float)):
            return float(obj) if isinstance(obj, float) else int(obj)
        elif isinstance(obj, str):
            return str(obj)
        elif isinstance(obj, (list, tuple)):
            return [json_serializer(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(k): json_serializer(v) for k, v in obj.items()}
        elif obj is None:
            return None
        elif hasattr(obj, '__dict__'):
            return {str(k): json_serializer(v) for k, v in obj.__dict__.items()}
        elif hasattr(obj, 'value'):  # For enum types
            return obj.value
        else:
            return str(obj)
    
    # Save task results
    task_results = []
    for result in results:
        task_result = {
            "task_id": str(result.task_id),
            "success": bool(result.success),
            "accuracy": float(result.accuracy),
            "confidence": float(result.confidence),
            "processing_time": float(result.processing_time),
            "transformation_type": str(result.transformation.transformation_type) if result.transformation else None,
            "has_causal_explanation": bool(result.causal_explanation is not None),
            "has_internal_explanation": bool(result.internal_explanation is not None),
            "physics_simulation_used": bool(result.physics_simulation),
            "failure_analysis": str(result.failure_analysis.failure_type) if result.failure_analysis and hasattr(result.failure_analysis, 'failure_type') else None
        }
        task_results.append(task_result)
    
    results_filename = f"d:/DARWIN/ENHANCED_ALLA_RESULTS_{timestamp}.json"
    with open(results_filename, 'w') as f:
        json.dump(task_results, f, indent=2, default=json_serializer)
    logger.info(f"Task results saved to {results_filename}")
    
    # Save comprehensive report
    report_filename = f"d:/DARWIN/ENHANCED_ALLA_COGNITIVE_REPORT_{timestamp}.json"
    with open(report_filename, 'w') as f:
        json.dump(final_report, f, indent=2, default=str)
    logger.info(f"Comprehensive report saved to {report_filename}")
    
    # Save cognitive traces for top performing tasks
    cognitive_traces = []
    successful_results = [r for r in results if r.success and r.accuracy > 0.8]
    for result in successful_results[:10]:  # Top 10 successful tasks
        trace = {
            "task_id": result.task_id,
            "accuracy": result.accuracy,
            "confidence": result.confidence,
            "advanced_processing": result.physics_simulation.get("advanced_processing", {}),
            "meta_strategies": result.physics_simulation.get("meta_strategies", {})
        }
        cognitive_traces.append(trace)
    
    traces_filename = f"d:/DARWIN/ENHANCED_ALLA_COGNITIVE_TRACES_{timestamp}.json"
    with open(traces_filename, 'w') as f:
        json.dump(cognitive_traces, f, indent=2, default=str)
    logger.info(f"Cognitive traces saved to {traces_filename}")

def print_final_summary(results, final_report):
    """Print comprehensive final summary"""
    
    print("\n" + "="*80)
    print("ENHANCED ALLA COGNITIVE ARCHITECTURE - FINAL RESULTS")
    print("="*80)
    
    # Basic statistics
    total_tasks = len(results)
    successful_tasks = sum(1 for r in results if r.success)
    success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0
    
    print(f"\nOVERALL PERFORMANCE:")
    print(f"   Total Tasks Processed: {total_tasks}")
    print(f"   Successful Tasks: {successful_tasks}")
    print(f"   Success Rate: {success_rate:.2%}")
    
    if results:
        avg_accuracy = sum(r.accuracy for r in results) / len(results)
        avg_confidence = sum(r.confidence for r in results) / len(results)
        avg_processing_time = sum(r.processing_time for r in results) / len(results)
        
        print(f"   Average Accuracy: {avg_accuracy:.2%}")
        print(f"   Average Confidence: {avg_confidence:.2f}")
        print(f"   Average Processing Time: {avg_processing_time:.2f}s")
    
    # Cognitive component analysis
    print(f"\n🧩 COGNITIVE COMPONENT USAGE:")
    component_usage = final_report.get("cognitive_component_analysis", {}).get("component_usage", {})
    for component, usage in component_usage.items():
        print(f"   {component.replace('_', ' ').title()}: {usage} times")
    
    # Quality metrics
    print(f"\n🎯 REASONING QUALITY METRICS:")
    quality_metrics = final_report.get("cognitive_component_analysis", {})
    print(f"   Explanation Quality: {quality_metrics.get('explanation_quality', 0):.2f}")
    print(f"   Causal Understanding: {quality_metrics.get('causal_understanding', 0):.2f}")
    print(f"   Physics Accuracy: {quality_metrics.get('physics_accuracy', 0):.2f}")
    print(f"   Pattern Recognition: {quality_metrics.get('pattern_recognition_rate', 0):.2f}")
    
    # Meta-learning insights
    print(f"\n🧬 META-LEARNING INSIGHTS:")
    meta_insights = final_report.get("meta_learning_insights", {})
    if meta_insights:
        print(f"   Meta-Patterns Discovered: {meta_insights.get('meta_patterns', {}).get('total_patterns', 0)}")
        print(f"   Recursive Hypotheses: {meta_insights.get('recursive_hypotheses', {}).get('total_hypotheses', 0)}")
        print(f"   Meta-Insights Generated: {meta_insights.get('meta_insights', {}).get('total_insights', 0)}")
    
    # Semantic understanding
    print(f"\n🌱 SEMANTIC UNDERSTANDING:")
    semantic_summary = final_report.get("semantic_understanding", {})
    if semantic_summary:
        print(f"   Concepts Learned: {semantic_summary.get('total_concepts', 0)}")
        print(f"   Concepts with Language: {semantic_summary.get('concepts_with_language', 0)}")
        print(f"   Average Concept Confidence: {semantic_summary.get('average_confidence', 0):.2f}")
    
    # Error analysis
    print(f"\n🔍 ERROR ANALYSIS:")
    error_analysis = final_report.get("error_analysis", {})
    if error_analysis:
        print(f"   Total Errors Analyzed: {error_analysis.get('total_errors_analyzed', 0)}")
        most_common_errors = error_analysis.get("most_common_error_types", [])
        if most_common_errors:
            print(f"   Most Common Error: {most_common_errors[0][0]} ({most_common_errors[0][1]} occurrences)")
    
    # Performance trends
    print(f"\n📈 PERFORMANCE TRENDS:")
    trends = final_report.get("performance_trends", {})
    if trends and trends.get("accuracy_trend") != "insufficient_data":
        print(f"   Accuracy Trend: {trends.get('accuracy_trend', 'unknown').title()}")
        print(f"   Confidence Trend: {trends.get('confidence_trend', 'unknown').title()}")
        recent_perf = trends.get("recent_performance", {})
        if recent_perf:
            print(f"   Recent Success Rate: {recent_perf.get('success_rate', 0):.2%}")
    
    # Recommendations
    print(f"\n💡 LEARNING RECOMMENDATIONS:")
    recommendations = final_report.get("recommendations", [])
    for i, rec in enumerate(recommendations[:5], 1):  # Top 5 recommendations
        print(f"   {i}. {rec}")
    
    # Best performing tasks
    print(f"\n🏆 TOP PERFORMING TASKS:")
    best_tasks = sorted([r for r in results if r.success], key=lambda x: x.accuracy, reverse=True)[:5]
    for i, task in enumerate(best_tasks, 1):
        print(f"   {i}. {task.task_id}: {task.accuracy:.2%} accuracy, {task.confidence:.2f} confidence")
    
    print("\n" + "="*80)
    print("🚀 Enhanced ALLA Cognitive Architecture Analysis Complete!")
    print("="*80)

def main():
    """Main function to run Enhanced ALLA"""
    
    print("🧠 Enhanced ALLA Cognitive Architecture")
    print("Human-Level Reasoning for ARC-2 Tasks")
    print("="*50)
    
    try:
        results, final_report = run_enhanced_alla_on_arc_dataset()
        
        print(f"\n✅ Enhanced ALLA execution completed successfully!")
        print(f"📈 Processed {len(results)} tasks with advanced cognitive reasoning")
        
        return results, final_report
        
    except Exception as e:
        print(f"\n💥 Enhanced ALLA execution failed: {e}")
        logger.error(f"Enhanced ALLA execution failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
