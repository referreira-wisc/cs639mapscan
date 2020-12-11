using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace MapLabeler
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Random random = new Random();
        private string[] classes = { "urban", "forest", "crop1", "crop2", "crop3", "river", "lake", "grass" };
        private int width = 224, height = 224;
        private string filename;
        private string imageFilePath;
        private object[] res;
        private int clusters;

        private MLApp.MLApp matlab;

        private List<Rectangle> rects;
        private List<ComboBox> comboBoxes;

        public MainWindow()
        {
            InitializeComponent();

            matlab = new MLApp.MLApp();
            matlab.Execute(@"cd C:\Users\repfe\Desktop\CS639Project");

            rects = new List<Rectangle>();
            comboBoxes = new List<ComboBox>();
            for (int i = 0; i < classes.Length; i++)
            {
                Rectangle rect = new Rectangle();
                rect.Name = "rect" + (i + 1);
                rect.Fill = Brushes.White;
                rect.Width = 60;
                rect.Height = 60;
                rect.Stroke = Brushes.Black;
                rect.VerticalAlignment = VerticalAlignment.Top;
                rect.Margin = new Thickness(0, 20 + (rect.Width + 20) * i, 0, 0);
                rect.SetValue(Grid.ColumnProperty, 3);
                rect.SetValue(Grid.RowProperty, 0);
                rect.Visibility = Visibility.Hidden;
                rect.MouseEnter += Rect_MouseEnter;
                rect.MouseLeave += Rect_MouseLeave;
                rects.Add(rect);
                MainGrid.Children.Add(rect);

                ComboBox comboBox = new ComboBox();
                comboBox.VerticalAlignment = VerticalAlignment.Top;
                comboBox.Margin = new Thickness(0, 40 + (rect.Width + 20) * i, 0, 0);
                comboBox.SetValue(Grid.ColumnProperty, 4);
                comboBox.SetValue(Grid.RowProperty, 0);
                foreach (string c in classes)
                {
                    ComboBoxItem item = new ComboBoxItem();
                    item.Content = c;
                    comboBox.Items.Add(item);
                }
                comboBox.Visibility = Visibility.Hidden;
                comboBox.SelectionChanged += ClassComboBox_SelectionChanged;
                comboBoxes.Add(comboBox);
                MainGrid.Children.Add(comboBox);
            }


            GetRandomSatelliteImage();
        }

        private void Rect_MouseEnter(object sender, MouseEventArgs e)
        {
            byte[,] overlay = (byte[,])res[0];
            byte[,] labels = (byte[,])res[1];
            byte rectIdx = byte.Parse(((Rectangle)sender).Name[4].ToString());
            byte[] pixels = new byte[width * height * 3];
            for (int i = 0; i < width * height * 3; i++)
            {
                int w = (i / 3) % height;
                int h = (i / 3) / height;
                if (labels[h, w] == rectIdx)
                    pixels[i] = overlay[i, 0];
            }
            BitmapSource bitmapSource = BitmapSource.Create(width, height, 96, 96, PixelFormats.Rgb24, BitmapPalettes.Halftone256, pixels, width * 3);
            ImgResult.Source = bitmapSource;
        }

        private void Rect_MouseLeave(object sender, MouseEventArgs e)
        {
            byte[,] overlay = (byte[,])res[0];
            byte[] pixels = new byte[width * height * 3];
            for (int i = 0; i < width * height * 3; i++)
                pixels[i] = overlay[i, 0];
            BitmapSource bitmapSource = BitmapSource.Create(width, height, 96, 96, PixelFormats.Rgb24, BitmapPalettes.Halftone256, pixels, width * 3);
            ImgResult.Source = bitmapSource;
        }

        private void ClassComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            int numberOfSelected = 0;
            for (int i = 0; i < clusters; i++)
                if (comboBoxes[i].SelectedIndex != -1)
                    numberOfSelected++;
            if (numberOfSelected == clusters)
                SaveButton.IsEnabled = true;
        }

        private void GetRandomSatelliteImage()
        {
            double minLong = -89.6313, maxLong = -87.8309;
            double minLat = 42.2897, maxLat = 44.3515;
            double longitude = random.NextDouble() * (maxLong - minLong) + minLong;
            double latitude = random.NextDouble() * (maxLat - minLat) + minLat;
            Console.WriteLine(longitude + ", " + latitude);
            filename = "i" + longitude + "," + latitude;

            string remoteFileUrl = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/";
            remoteFileUrl += longitude + "," + latitude;
            remoteFileUrl += ",13.5,0/224x238?access_token=";
            remoteFileUrl += "pk.eyJ1IjoicmVwZmVycmVpcmEiLCJhIjoiY2l5dmo3ZmxjMDAyZTJxbjM2c2NvaWluZSJ9.hg6bkbnvwfKAa6VS0kNhCg";
            string imageFilename = filename + ".jpg";
            imageFilePath = System.IO.Path.Combine(@"D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\images", imageFilename);
            WebClient webClient = new WebClient();
            webClient.DownloadFile(remoteFileUrl, imageFilePath);
            object result = null;
            matlab.Feval("removeWatermark", 0, out result, imageFilePath);
            ImgInput.Source = new BitmapImage(new Uri(imageFilePath));
        }

        private void ClustersComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ClustersComboBox.SelectedIndex == -1)
                return;
            clusters = int.Parse(((ComboBoxItem)ClustersComboBox.SelectedItem).Content.ToString());

            object result = null;
            matlab.Feval("kmeansCluster", 3, out result, (double)clusters, imageFilePath);
            res = result as object[];
            byte[,] overlay = (byte[,])res[0];
            byte[] pixels = new byte[width * height * 3];
            for (int i = 0; i < width * height * 3; i++)
                pixels[i] = overlay[i, 0];
            BitmapSource bitmapSource = BitmapSource.Create(width, height, 96, 96, PixelFormats.Rgb24, BitmapPalettes.Halftone256, pixels, width * 3);
            ImgResult.Source = bitmapSource;

            for (int i = 0; i < classes.Length; i++)
            {
                rects[i].Visibility = Visibility.Hidden;
                comboBoxes[i].Visibility = Visibility.Hidden;
            }
            double[,] colors = (double[,])res[2];
            for (int i = 0; i < clusters; i++)
            {
                Rectangle rect = rects[i];
                rect.Fill = new SolidColorBrush(Color.FromArgb((byte)192, (byte)(colors[i, 0] * 255), (byte)(colors[i, 1] * 255), (byte)(colors[i, 2] * 255)));
                rect.Visibility = Visibility.Visible;
                ComboBox comboBox = comboBoxes[i];
                comboBox.Visibility = Visibility.Visible;
            }
        }

        private void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            byte[,] labels = (byte[,])res[1];
            byte[,] mask = new byte[width, height];
            for (int c = 0; c < clusters; c++)
                for (int i = 0; i < height; i++)
                    for (int j = 0; j < width; j++)
                        if (labels[i, j] == c + 1)
                            mask[i, j] = (byte)comboBoxes[c].SelectedIndex;

            string[] lines = new string[height];
            for (int i = 0; i < height; i++)
            {
                string line = "";
                for (int j = 0; j < width; j++)
                {
                    line += mask[i, j].ToString();
                }
                lines[i] = line;
            }

            string maskFilename = filename + ".txt";
            string maskFilePath = System.IO.Path.Combine(@"D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks", maskFilename);
            File.WriteAllLines(maskFilePath, lines);

            SaveButton.IsEnabled = false;
            ClustersComboBox.SelectedIndex = -1;
            ImgResult.Source = null;
            for (int i = 0; i < classes.Length; i++)
            {
                rects[i].Visibility = Visibility.Hidden;
                comboBoxes[i].Visibility = Visibility.Hidden;
            }

            GetRandomSatelliteImage();
        }

        private void SkipButton_Click(object sender, RoutedEventArgs e)
        {
            SaveButton.IsEnabled = false;
            ClustersComboBox.SelectedIndex = -1;
            ImgResult.Source = null;
            for (int i = 0; i < classes.Length; i++)
            {
                rects[i].Visibility = Visibility.Hidden;
                comboBoxes[i].Visibility = Visibility.Hidden;
            }

            GetRandomSatelliteImage();
        }
    }
}
