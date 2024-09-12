import unreal
import json
import re


level_sequence_path = '/Game/Sequence/Live/cam_5.cam_5'
# level_sequence_path = '/Game/Sequence/Live/Sng026/LS_Sng026_Common_Camera.LS_Sng026_Common_Camera'
# level_sequence_path = '/Game/Sequence/Live/Sng026/NewLevelSequence.NewLevelSequence'
level_sequence = unreal.load_asset(level_sequence_path)
target_sequence_path = '/Game/Sequence/Live/cam_5_cc.cam_5_cc'
target_level_sequence = unreal.load_asset(target_sequence_path)

def hh(ee):
    print(ee)
    for e in dir(ee):
        if not e.startswith('_'):print(e)

def copy_sequence(source_sequence,target_sequence):

    
    for source_bindings in source_sequence.get_bindings():

        movie_scene = target_sequence.get_movie_scene()

        sequencer_tools = unreal.SequencerTools()

        editor_level_lib = unreal.EditorLevelLibrary()

        camera_actor = editor_level_lib.spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
        camera_binding = target_sequence.add_spawnable_from_instance(camera_actor)
        camera_component_binding = target_sequence.add_possessable(camera_actor.get_cine_camera_component())
        camera_component_binding.set_parent(camera_binding)

        focal_length_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
        focal_length_track.set_property_name_and_path('Current Focal Length', 'CurrentFocalLength')
        focal_length_section = focal_length_track.add_section()
        focal_length_section.set_start_frame_bounded(0)
        focal_length_section.set_end_frame_bounded(0)	

        camera_transform_track = camera_binding.add_track(unreal.MovieScene3DTransformTrack)

        print(camera_actor)
        hh(target_sequence)
        unreal.EditorLevelLibrary.destroy_actor(camera_actor)
        movie_scene.remove_possessable(camera_binding.get_binding_id())
        # sequencer_tools.remove_possessable(camera_binding.get_binding_id())
        raise

copy_sequence(level_sequence,target_level_sequence)