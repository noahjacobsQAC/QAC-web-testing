
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

class imgutils:

    @staticmethod
    def highlight_element(_driver: webdriver, _element : WebElement, _color, _thickness: int):
        
        #driver = _element._parent
        def apply_style(style):
            _driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",_element, style)

        apply_style("border: " + str(_thickness) + "px solid " + _color + ";")


    @staticmethod
    def unhighlight_element(_driver: webdriver, _element : WebElement):
        #driver = _element._parent
        def apply_style(style):
            _driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",_element, style)

        apply_style("border: " + str(0) + "px solid " + "red" + ";")

    @staticmethod
    def scroll_to_top_of_page_with_JS(_driver: webdriver):
        javaScript = "window.scrollTo(0, 0);"
        _driver.execute_script(javaScript)

    @staticmethod
    def scroll_to_Coordinate_Y(_driver: webdriver, _y_value: int):
        None

        javaScript = "window.scrollTo(" + str(0) + ", " + str(_y_value) + ");"
        _driver.execute_script(javaScript)

    # This functions scrolls to _element and screenshots it
    # @param _driver the WebDriver
    # @param _element the WebElement
    # @param _id the id to print on the image and use in the filename
    @staticmethod
    def scrollAndScreenshotElement(_driver: webdriver ,_element: WebElement,_id):
        
        if _element.is_enabled():
            imgutils.scroll_to_top_of_page_with_JS(_driver)

            y_scroll_value = _element.location.get('y')
            imgutils.scroll_to_Coordinate_Y(_driver, y_scroll_value - 30)

            file_path = r'.\\screenshots\\'
            #print("Saving screenshot to: " + file_path + "screenshot_" + str(_id) + ".png")
            _driver.save_screenshot(file_path + "screenshot_" + str(_id) + ".png")
            imgutils.unhighlight_element(_driver, _element)
            return (file_path + "screenshot_" + str(_id) + ".png")

            # TODO: imprint the image location on the file
            '''
                BufferedImage screenshotImage = ImageIO.read(new ByteArrayInputStream(img_bytes));
                    
                    // add some text and draw a rectangle
                    Graphics graphicsObject = screenshotImage.getGraphics();
                    graphicsObject.setColor(Color.red);
                    graphicsObject.setFont(new Font( "SansSerif", Font.BOLD, 16));
                    
                    graphicsObject.drawRect(0, 0, 50, 20);
                    
                    graphicsObject.drawString("id: " + _id, 0, 16);
                    
                    graphicsObject.dispose();

                    long webElementID = getNextUniqueID();
                    String webElementIDString = (webElementID <= 9)? "0" + webElementID : "" + webElementID ;
                    String screnshotName = filePath + webElementIDString + " - id-" + _id +  " - " + getTimeStamp() + ".png";
                    // save the image
                    File screenshotFile = new File(screnshotName);
                    System.out.println("screenshot path: " + screnshotName);
                    screenshotFile.mkdirs();
                    ImageIO.write(screenshotImage, "png", screenshotFile);

                } 
                catch (IOException ioException) 
                {
                    ioException.printStackTrace();
                }
                
            }
            else
            {
                System.out.println("1 Element found was invisible... skipping screenshot. had text: \"" + _element.getText() + "\"");
            }
        }
            '''