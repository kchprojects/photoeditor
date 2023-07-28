#include <opencv2/opencv.hpp>
int add(int i, int j);

namespace phe
{
    void show(const cv::Mat& img){
        cv::namedWindow("mat",cv::WINDOW_NORMAL);
        cv::imshow("mat",img);
        cv::waitKey();
    }

    cv::Mat identity(const cv::Mat& img){
        return img;
    }

} // namespace phe


