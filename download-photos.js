/**
 * 下载上海著名建筑的真实照片
 * 使用多个来源确保下载成功
 */
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const photosDir = path.join(__dirname, 'photos');
if (!fs.existsSync(photosDir)) fs.mkdirSync(photosDir, { recursive: true });

// 多个备选URL来源，按优先级排列
const photoSources = [
  // Building 1: Peace Hotel (1929)
  {
    name: '01-peace-hotel.jpg',
    urls: [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Peace_Hotel_Shanghai.jpg/800px-Peace_Hotel_Shanghai.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Peace_Hotel%2C_Bund%2C_Shanghai.jpg/800px-Peace_Hotel%2C_Bund%2C_Shanghai.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Peace_Hotel_2009.jpg/800px-Peace_Hotel_2009.jpg'
    ]
  },
  // Building 2: Oriental Pearl Tower (1995)
  {
    name: '02-oriental-pearl.jpg',
    urls: [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Oriental_Pearl_Tower_2020.jpg/800px-Oriental_Pearl_Tower_2020.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Oriental_Pearl_Tower_Shanghai_2019.jpg/800px-Oriental_Pearl_Tower_Shanghai_2019.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Oriental_Pearl_Tower.JPG/800px-Oriental_Pearl_Tower.JPG'
    ]
  },
  // Building 3: Jin Mao Tower (1999)
  {
    name: '03-jinmao.jpg',
    urls: [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Jin_Mao_Tower_2015.jpg/800px-Jin_Mao_Tower_2015.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jin_Mao_Tower_2020.jpg/800px-Jin_Mao_Tower_2020.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Jinmao_Tower_Shanghai.jpg/800px-Jinmao_Tower_Shanghai.jpg'
    ]
  },
  // Building 4: Shanghai WFC (2008)
  {
    name: '04-swfc.jpg',
    urls: [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Shanghai_World_Financial_Center_2015.jpg/800px-Shanghai_World_Financial_Center_2015.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Shanghai_World_Financial_Center_2008.jpg/800px-Shanghai_World_Financial_Center_2008.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/SWFC_Shanghai_2010.jpg/800px-SWFC_Shanghai_2010.jpg'
    ]
  },
  // Building 5: China Art Museum (2010)
  {
    name: '05-china-art-museum.jpg',
    urls: [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/China_Art_Museum_Shanghai_2019.jpg/800px-China_Art_Museum_Shanghai_2019.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/China_Art_Museum_2021.jpg/800px-China_Art_Museum_2021.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/China_Art_Museum_-_Expo_2010.jpg/800px-China_Art_Museum_-_Expo_2010.jpg'
    ]
  },
  // Building 6: Shanghai Tower (2015)
  {
    name: '06-shanghai-tower.jpg',
    urls: [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Shanghai_Tower_2015.jpg/800px-Shanghai_Tower_2015.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Shanghai_Tower_2021.jpg/800px-Shanghai_Tower_2021.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Shanghai_Tower_2020.jpg/800px-Shanghai_Tower_2020.jpg'
    ]
  }
];

function downloadFile(url, filePath) {
  return new Promise((resolve) => {
    const protocol = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(filePath);
    
    const req = protocol.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/jpeg,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
      },
      timeout: 15000
    }, (response) => {
      // Handle redirects
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        file.close();
        fs.unlink(filePath, () => {});
        const redirectUrl = response.headers.location.startsWith('http') 
          ? response.headers.location 
          : new URL(response.headers.location, url).href;
        downloadFile(redirectUrl, filePath).then(resolve);
        return;
      }
      
      if (response.statusCode !== 200) {
        file.close();
        fs.unlink(filePath, () => {});
        resolve(false);
        return;
      }
      
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        // Check if file has content (not HTML error page)
        const stats = fs.statSync(filePath);
        if (stats.size > 5000) {
          resolve(true);
        } else {
          fs.unlink(filePath, () => {});
          resolve(false);
        }
      });
    });
    
    req.on('error', () => {
      file.close();
      fs.unlink(filePath, () => {});
      resolve(false);
    });
    
    req.on('timeout', () => {
      req.destroy();
      file.close();
      fs.unlink(filePath, () => {});
      resolve(false);
    });
  });
}

async function downloadAll() {
  console.log('=== 下载上海建筑照片 ===\n');
  
  let success = 0;
  let failed = 0;
  
  for (const item of photoSources) {
    const filePath = path.join(photosDir, item.name);
    
    // Skip if file already exists and has content
    if (fs.existsSync(filePath)) {
      const stats = fs.statSync(filePath);
      if (stats.size > 5000) {
        console.log(`[SKIP] ${item.name} (already exists, ${Math.round(stats.size/1024)}KB)`);
        success++;
        continue;
      }
    }
    
    console.log(`Downloading ${item.name}...`);
    let downloaded = false;
    
    for (const url of item.urls) {
      console.log(`  Trying: ${url.substring(0, 70)}...`);
      const result = await downloadFile(url, filePath);
      if (result) {
        const stats = fs.statSync(filePath);
        console.log(`  ✓ SUCCESS (${Math.round(stats.size/1024)}KB)`);
        downloaded = true;
        break;
      }
      console.log(`  ✗ Failed, trying next source...`);
    }
    
    if (downloaded) {
      success++;
    } else {
      failed++;
      console.log(`  ✗ ALL SOURCES FAILED for ${item.name}`);
    }
  }
  
  console.log(`\n=== 完成: ${success} success, ${failed} failed ===`);
}

downloadAll().catch(console.error);