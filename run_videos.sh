video="video_1.mp4 video_3.mp4 video_4.mp4 video_5.mp4 video_6.mp4 video_7.mp4 video_8.mp4"

input_video/video_2.mp4

for v in $video;
do
  input=input_video/"$v"
  output=output_video/"$v"
  python main.py --input-video "$input" --output "$output" 

  rm -r results

python main.py --input-video input_video/video_1.mp4 --output output_video/video_1.mp4
python main.py --input-video input_video/video_3.mp4 --output output_video/video_3.mp4 # **

python main.py --input-video input_video/video_4.mp4 --output output_video/video_4.mp4
python main.py --input-video input_video/video_5.mp4 --output output_video/video_5.mp4
python main.py --input-video input_video/video_6.mp4 --output output_video/video_6.mp4 # 保留
python main.py --input-video input_video/video_7.mp4 --output output_video/video_7.mp4
python main.py --input-video input_video/video_8.mp4 --output output_video/video_8.mp4
